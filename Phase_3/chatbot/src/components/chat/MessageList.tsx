"use client";

import { Message } from "@/types/chat";

interface MessageListProps {
  messages: Message[];
}

export default function MessageList({ messages }: MessageListProps) {
  return (
    <div className="space-y-4">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
        >
          <div
            className={`max-w-[80%] rounded-2xl px-4 py-3 ${
              message.role === "user"
                ? "bg-purple-600 text-white"
                : "bg-gray-100 text-gray-800"
            }`}
          >
            <div className="text-sm font-semibold mb-1 opacity-70">
              {message.role === "user" ? "You" : "Assistant"}
            </div>
            <div className="whitespace-pre-wrap">{message.content}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
