"use client";
import React, { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';

export default function SettingsPage() {
  const [health, setHealth] = useState<string>('Checking...');
  const [apiKey, setApiKey] = useState<string>('');
  const [copied, setCopied] = useState<boolean>(false);

  useEffect(() => {
    const url = process.env.NEXT_PUBLIC_MCP_SERVER_URL;
    if (!url) {
      setHealth('No MCP_SERVER_URL configured');
      return;
    }
    fetch(`${url}/health`)
      .then((res) => {
        if (res.ok) setHealth('Connected');
        else setHealth(`Error ${res.status}`);
      })
      .catch((_) => setHealth('Disconnected'));
  }, []);

  const generateKey = () => {
    const key = crypto.randomUUID();
    setApiKey(key);
    setCopied(false);
  };

  const copyToClipboard = () => {
    if (!apiKey) return;
    navigator.clipboard.writeText(apiKey);
    setCopied(true);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Settings</h1>
      <div className="mb-4">
        <strong>Server Health:</strong> {health}
      </div>
      <div className="mb-4">
        <Button onClick={generateKey}>Generate API Key</Button>
      </div>
      {apiKey && (
        <div className="flex items-center space-x-2">
          <input
            type="text"
            readOnly
            value={apiKey}
            className="flex-1 p-2 border rounded"
          />
          <Button onClick={copyToClipboard} variant="secondary">
            {copied ? 'Copied' : 'Copy'}
          </Button>
        </div>
      )}
    </div>
  );
}