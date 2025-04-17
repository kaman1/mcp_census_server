'use server';

import { createStreamableValue } from 'ai/rsc';
import { CoreMessage, streamText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { Weather } from '@/components/weather';
import { generateText } from 'ai';
import { createStreamableUI } from 'ai/rsc';
import { ReactNode } from 'react';
import { z } from 'zod';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  display?: ReactNode;
}


// Streaming Chat 
export async function continueTextConversation(messages: CoreMessage[]) {
  const result = await streamText({
    model: openai('gpt-4-turbo'),
    messages,
  });

  const stream = createStreamableValue(result.textStream);
  return stream.value;
}

// Gen UIs 
export async function continueConversation(history: Message[]) {
  const stream = createStreamableUI();

  const { text, toolResults } = await generateText({
    model: openai('gpt-3.5-turbo'),
    system: 'You are a friendly AI assistant with access to weather and census data tools.',
    messages: history,
    tools: {
      showWeather: {
        description: 'Show the weather for a given location.',
        parameters: z.object({
          city: z.string().describe('The city to show the weather for.'),
          unit: z
            .enum(['F'])
            .describe('The unit to display the temperature in'),
        }),
        execute: async ({ city, unit }) => {
          stream.done(<Weather city={city} unit={unit} />);
          return `Here's the weather for ${city}!`;
        },
      },
      censusGet: {
        description: 'Retrieve data from the US Census Bureau via MCP server.',
        parameters: z.object({
          year: z.number().int().describe('Year of the census data, e.g. 2020'),
          dataset: z.string().describe('Dataset endpoint, e.g. "acs/acs5"'),
          get: z.array(z.string()).describe('Variables to retrieve, e.g. ["P001001"]'),
          for: z.string().describe('Geography spec, e.g. "state:06"'),
          key: z.string().optional().describe('Optional Census API key override'),
        }),
        execute: async (args) => {
          const { year, dataset, get, for: geo, key } = args as any;
          const body = {
            jsonrpc: '2.0',
            id: Date.now().toString(),
            method: 'tools/call',
            params: {
              name: 'census/get',
              arguments: { year, dataset, get, for: geo, key },
            },
          };
          const res = await fetch(`${process.env.NEXT_PUBLIC_MCP_SERVER_URL}/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            'X-API-Key': process.env.NEXT_PUBLIC_SERVER_API_KEY || '',
            },
            body: JSON.stringify(body),
          });
          const json = await res.json();
          const text = json.result?.content?.[0]?.text;
          return text || JSON.stringify(json);
        },
      },
    },
  });

  return {
    messages: [
      ...history,
      {
        role: 'assistant' as const,
        content:
          text || toolResults.map(toolResult => toolResult.result).join(),
        display: stream.value,
      },
    ],
  };
}

// Utils
export async function checkAIAvailability() {
  const envVarExists = !!process.env.OPENAI_API_KEY;
  return envVarExists;
}