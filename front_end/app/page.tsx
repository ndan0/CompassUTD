"use client";
import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import ChatDemo from "../components/chat_demo";
import axios from "axios";

type Props = {};

export default function IndexPage({}: Props) {
  const [pageCount, setPageCount] = React.useState<any>(0);
  const [messageCount, setMessageCount] = React.useState(0);

  function time_diff(providedDate: any) {
    console.log(providedDate)
    var currentDate = new Date();
  
    // Calculate the time difference in milliseconds
    var difference = currentDate.getTime() - providedDate * 1000;
  
    // Calculate the time difference in hours, minutes, and seconds
    var hours = Math.floor(difference / (1000 * 60 * 60));
    var minutes = Math.floor((difference / (1000 * 60)) % 60);
    var seconds = Math.floor((difference / 1000) % 60);
  
    // Determine the most relevant unit
    var closestUnit;
    var closestValue;
    if (hours > 0) {
      closestUnit = "hours";
      closestValue = hours;
    } else if (minutes > 0) {
      closestUnit = "minutes";
      closestValue = minutes;
    } else {
      closestUnit = "seconds";
      closestValue = seconds;
    }
  
    return closestValue + " " + closestUnit;
  }
  
  React.useEffect(() => {
    async function executeRequests() {
      try {
        const [response2, response3] = await Promise.all([
          axios.get("/api/id"),
          axios.get("/api/messages"),
        ]);

        console.log(response2.data);
        setPageCount(response2.data.body);
        setMessageCount(response3.data.body.count);
      } catch (error) {
        console.error(error);
      }
    }

    executeRequests();
  }, []);

  return (
    <section className="container grid items-center gap-6 pb-8 pt-6 md:py-10">
      <div className="flex flex-col items-center gap-10">
        <div className="flex flex-col gap-5 items-center">
          <div className="font-bold flex flex-wrap justify-center items-center tracking-tight text-4xl md:text-6xl lg:text-8xl">
            <span className="grad-text flex-shrink">UTD </span><span className="invisible">i</span>
            <span className="inline-block">
            <span className="grad-text">College</span><span className="invisible">i</span>
            <span className="grad-text">Advisor</span>
            </span>
          </div>
          <Badge className="w-fit">Public Beta out now</Badge>
        </div>
        <Link
          className="group flex flex-1 items-center justify-center"
          href="/chat"
        >
          <div className="flex gap-2 flex-wrap justify-center">
            <div className="hidden w-[150px] flex-col sm:flex justify-center font-bold tracking-tight grad-text text-2xl z-10">
              <div className="transition opacity-100 ease-in-out">
                <div className="text-base">
                  {pageCount !== 0 && (
                    <>
                      <span className="inline-block text-2xl pb-1 my-1 border-b border-slate-500 border-opacity-30">
                        Recent Users
                      </span>
                      {pageCount.documents.map((object: any) => (
                        <div key={object.time}>
                          {time_diff(object.time)} ago
                        </div>
                      ))}
                    </>
                  )}
                </div>
              </div>
            </div>
            <div className="relative flex-1 md:w-[450px] lg:w-[500px] max-w-[500px] md:p-5 h-[300px] md:h-[400px] transition-all ease-in-out">
              <ChatDemo />
              <div className="dark-shadow" />
              <div className="absolute z-10 left-0 right-0 top-0 bottom-0 m-auto flex justify-center items-center">
            <Button
              className="shadow-white text-base text-bold text-black"
              size={"lg"}
            >
              Get Started
            </Button>
          </div>
            </div>
            <div className="w-full lg:w-[150px] flex justify-evenly font-bold tracking-tight grad-text text-2xl z-10 mt-10 lg:mt-20">
              {pageCount !== 0 && messageCount !== 0 && (
                <div className="flex-row flex-1 flex justify-evenly lg:justify-end lg:flex-col w-full">
                  <div className="transition opacity-100 ease-in-out py-2 lg:border-b border-slate-500 border-opacity-30">
                    <span className="flex items-center mr-1 text-4xl">
                      {pageCount.count}+
                    </span>
                    <span className="inline-block text-lg">Users</span>
                  </div>
                  <div className="transition opacity-100 ease-in-out py-2">
                    <span className="flex items-center mr-1 text-4xl">
                      {messageCount}+
                    </span>
                    <span className="inline-block text-lg">Messages Sent</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </Link>
        <div className="flex flex-col items-center gap-1">
          <div className="font-medium text-xl">Powered By</div>
          <div className="font-bold tracking-tight text-2xl md:text-4xl lg:text-6xl">
            💪 <span className="grad-text">Vertex AI</span> +{" "}
            <span className="grad-text">Langchain</span> 🦜
          </div>
        </div>
        <Badge variant={"outline"} className="text-sm font-medium">
          Website designed by Arihan Varanasi
        </Badge>
      </div>
    </section>
  );
}
