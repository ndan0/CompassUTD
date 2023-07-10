"use client";
import React from "react";
import { MoreVertical } from "lucide-react";
import { Badge } from "./ui/badge";
import { Avatar, AvatarImage, AvatarFallback } from "./ui/avatar";
import { atom } from "jotai";
import HistorySelect from "./historySelect";
import ChatMessages from "./chatMessages";
import {
  Popover,
  PopoverTrigger,
} from "@/components/ui/popover";

export const conversationIdAtom = atom("New Chat");
export const dateAtom = atom("New Chat")

export type Message = {
  id: number;
  text: string;
};

export default function ChatDemo() {
  const [messages, setMessages] = React.useState<Message[]>([]);
  const [completedTyping, setCompletedTyping] = React.useState(false);
  const [displayResponse, setDisplayResponse] = React.useState("");

  React.useEffect(() => {
    setMessages([
        {
          id: 0,
          text: "Hi! I'm Temoc, your unofficial College Advising assistant. Please note that my responses may not always be entirely accurate. How can I help?",
        },
      ]);
  }, []);

  React.useEffect(() => {
    setCompletedTyping(false);
    setDisplayResponse("");

    if (messages.length === 0) {
      return;
    }

    let i = 0;
    const words =
      messages[messages.length - 1].id === 0
        ? messages[messages.length - 1].text.split(" ")
        : [];

    const intervalId = setInterval(() => {
      setDisplayResponse(words.slice(0, i).join(" "));
      i++;

      if (i > words.length) {
        clearInterval(intervalId);
        setCompletedTyping(true);
      }
    }, 60);

    return () => clearInterval(intervalId);
  }, [messages]);

  return (
    <div className="h-full border-gray-700 w-full rounded-xl border p-1">
      <div className="border border-gray-700 h-full w-full rounded-lg flex flex-col">
        <div className="w-full bg-orange-800 p-2 border-b border-gray-700 rounded-t-md flex justify-between items-center">
          <div className="flex gap-2 items-center font-semibold tracking-tight">
            <Avatar>
              <AvatarImage
                className="object-cover"
                src="https://cometlife.org/wp-content/uploads/2019/10/utdallas_19489995-300x200.jpg"
              />
              <AvatarFallback>TM</AvatarFallback>
            </Avatar>
            CompassUTD
            <HistorySelect />
            <Popover>
              <PopoverTrigger>
                <MoreVertical />
              </PopoverTrigger>
            </Popover>
          </div>
          <Badge
            variant={"secondary"}
            className="bg-green-100 sm:flex gap-1 justify-center items-center text-black pointer-events-none border-green-50 hidden"
          >
            <div className="w-2 aspect-square rounded-full bg-green-500 animate-pulse"></div>{" "}
            Online
          </Badge>
        </div>
        <div className="flex-1 p-2 overflow-scroll text-sm">
          <ChatMessages
            messages={messages}
            displayResponse={displayResponse}
            completedTyping={completedTyping}
          />
        </div>
      </div>
    </div>
  );
}
