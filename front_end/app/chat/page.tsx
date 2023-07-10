"use client";
import Chat from "@/components/chat";
import React from "react";
import axios from "axios";

export default function Home() {
  React.useEffect(() => {
    axios.post("/api/id").then((res) => {
      console.log(res.data);
    });
  }, []);

  return (
    <div className="flex justify-center h-[calc(100dvh)] items-center">
        <meta
          name="viewport"
          content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0"
        />
      <div className="max-w-[500px] w-full md:p-5 md:max-h-[700px] h-full">
        <Chat />
      </div>
    </div>
  );
}
