"use client";

import { useState, useRef, useEffect } from "react";
import ChatInput from "./ChatInput";
import MessageList from "./MessageList";
import { processUserMessage } from "@/lib/ai-agent";
import { Message } from "@/types/chat";

interface ChatInterfaceProps {
  userId: string;
}

export default function ChatInterface({ userId }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content: `Hello! I'm your AI-powered Todo assistant. I can help you manage your tasks using natural language.

Try saying things like:
- "Add a task to buy groceries"
- "Show me all my tasks"
- "Mark task #1 as done"
- "Delete task #3"
- "Update task #1 title to 'Buy organic groceries'"

What would you like to do today?`,
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Process with AI agent
      const response = await processUserMessage(userId, content);

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : "Unknown error"}. Please try again.`,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-2xl flex flex-col h-[80vh] max-w-4xl w-full overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-indigo-600 px-6 py-4 flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold text-white">Todo Chatbot</h1>
          <p className="text-purple-100 text-sm">User: {userId}</p>
        </div>
        <button
          onClick={() => window.location.reload()}
          className="text-white hover:text-purple-200 transition-colors"
        >
          Exit
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6">
        <MessageList messages={messages} />
        {isLoading && (
          <div className="flex items-center space-x-2 text-gray-500">
            <div className="animate-bounce">.</div>
            <div className="animate-bounce" style={{ animationDelay: "0.1s" }}>
              .
            </div>
            <div className="animate-bounce" style={{ animationDelay: "0.2s" }}>
              .
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-gray-200 p-4">
        <ChatInput onSend={handleSendMessage} disabled={isLoading} />
      </div>
    </div>
  );
}
