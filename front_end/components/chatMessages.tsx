"use static";
import React from "react";
import { Message } from "./chat";
import ReactMarkdown from "react-markdown";

interface Props {
  messages: Message[];
  displayResponse: string;
  completedTyping: boolean;
}

export default function ChatMessages({
  messages,
  displayResponse,
  completedTyping,
}: Props) {
  return (
    <>
      {messages.map((message, index) => (
        <div
          key={index}
          className={`flex break-words ${
            message.id === 1 ? "justify-end" : "justify-start"
          } mb-2`}
        >
          <div
            className={`rounded-lg p-2 bg-gray-200 dark:bg-gray-800 max-w-[70%] ${
              message.id === 0 && index === messages.length - 1
                ? "ml-2"
                : message.id === 0
                ? "ml-2"
                : "mr-2 mesUser"
            }`}
          >
            {message.id === 0 && index === messages.length - 1 ? (
              <div className="!text-sm">
                {displayResponse}
                {!completedTyping && (
                  <svg
                    viewBox="8 4 8 16"
                    xmlns="http://www.w3.org/2000/svg"
                    className="cursor !filter-invert"
                  >
                    <rect x="10" y="6" width="4" height="12" fill="#fff" />
                  </svg>
                )}
              </div>
            ) : (
              <p className="text-sm">
                <ReactMarkdown>{message.text}</ReactMarkdown>
              </p>
            )}
          </div>
        </div>
      ))}
    </>
  );
}
