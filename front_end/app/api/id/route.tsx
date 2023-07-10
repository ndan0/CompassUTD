import { NextResponse, NextRequest } from "next/server";
const { MongoClient, ServerApiVersion } = require("mongodb");
const uri = `mongodb+srv://${process.env.MONGODB_LOGIN}@${process.env.MONGODB_LOCATION}/?retryWrites=true&w=majority`;

export async function POST(req: NextRequest) {
  const client = new MongoClient(uri, {
    serverApi: {
      version: ServerApiVersion.v1,
      strict: true,
      deprecationErrors: true,
    },
  });

  async function run() {
    try {
      // Connect the client to the server (optional starting in v4.7)
      await client.connect();
      // Send a ping to confirm a successful connection
      // await client.db("views").command({ ping: 1 });

      const db = client.db("views");
      const collectionName = "views";
      const collection = db.collection(collectionName);

      // JSON data
      //get current epochs time to seconds
      const date = new Date();
      const seconds = Math.round(date.getTime() / 1000);
      const jsonData = {
        time: seconds,
      };
      await collection.insertOne(jsonData);
      console.log("Data inserted successfully!");
    } finally {
      // Ensures that the client will close when you finish/error
      await client.close();
    }
  }
  run().catch(console.dir);
  // const body = await req.json();
  // console.log(body.id);
  // const { searchParams } = new URL(req.url);
  // const userId = searchParams.get("id");
  return NextResponse.json({ status: 200 });
}

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
      const db = client.db("views");
      const collectionName = "views";
      const collection = db.collection(collectionName);

      // Get the total count
      const count = await collection.countDocuments();

      // Get the most recent 5 documents
      const documents = await collection
        .find({})
        .sort({ _id: -1 })
        .limit(5)
        .toArray();

      return { count, documents };
    } finally {
      await client.close();
    }
  }

  const result = await run().catch(console.dir);

  return NextResponse.json({ status: 200, body: result });
}
