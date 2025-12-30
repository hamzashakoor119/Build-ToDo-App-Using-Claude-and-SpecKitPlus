import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Todo Chatbot - AI-Powered Task Management",
  description: "Manage your tasks with natural language using AI",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
