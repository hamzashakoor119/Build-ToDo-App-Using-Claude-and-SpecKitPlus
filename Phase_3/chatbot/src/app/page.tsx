"use client";

import { useState } from "react";
import ChatInterface from "@/components/chat/ChatInterface";

export default function Home() {
  const [userId, setUserId] = useState("");

  return (
    <main className="min-h-screen flex items-center justify-center p-4">
      {!userId ? (
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full">
          <div className="text-center mb-6">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">
              Todo Chatbot
            </h1>
            <p className="text-gray-600">
              AI-Powered Task Management
            </p>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Enter your User ID
              </label>
              <input
                type="text"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder="e.g., user-123"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none"
              />
            </div>

            <button
              onClick={() => userId && setUserId(userId)}
              disabled={!userId}
              className="w-full bg-purple-600 text-white py-3 rounded-lg font-semibold hover:bg-purple-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              Start Chatting
            </button>

            <p className="text-xs text-gray-500 text-center mt-4">
              For demo purposes, use any user ID
            </p>
          </div>
        </div>
      ) : (
        <ChatInterface userId={userId} />
      )}
    </main>
  );
}
