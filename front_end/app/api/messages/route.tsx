import { NextResponse, NextRequest } from "next/server";
const { MongoClient, ServerApiVersion } = require("mongodb");
const uri =`mongodb+srv://${process.env.MONGODB_LOGIN}@${process.env.MONGODB_LOCATION}/?retryWrites=true&w=majority`;


export async function GET() {
    const client = new MongoClient(uri, {
      serverApi: {
        version: ServerApiVersion.v1,
        strict: true,
        deprecationErrors: true,
      },
    });
  
  
    async function run() {
      try {
        await client.connect();
        const db = client.db("chat_history");
        const collectionName = "message_store";
        const collection = db.collection(collectionName);
        const count = await collection.countDocuments();
        return count;
      } finally {
        await client.close();
      }
    }
    const count = await run().catch(console.dir);
    return NextResponse.json({ status: 200, body: { count } });
  }
  
  