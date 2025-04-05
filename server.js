import express from "express";
import mongoose from "mongoose";
import cors from "cors";
import bodyParser from "body-parser";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import Feedback from "./feedback.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(cors());
app.use(bodyParser.json());

const PORT = process.env.PORT || 3000;
const CSV_FILE = path.join(__dirname, "reviews.csv");

// MongoDB Connection
const connectDB = async () => {
  try {
    mongoose.connection.on("connected", () => console.log("MongoDB connected."));
    await mongoose.connect("mongodb+srv://sadityakumar194:12345@cluster0.hdmpeoz.mongodb.net/", {
      dbName: "chiler",
    });
  } catch (err) {
    console.error("DB connection failed:", err.message);
  }
};

connectDB();

// CSV Logging (Optional)
function writeToCSV(review) {
  const { name, event, reviewText, date } = review;
  const csvRow = `"${date}","${name}","${event}","${reviewText}"\n`;
  if (!fs.existsSync(CSV_FILE)) {
    fs.writeFileSync(CSV_FILE, `"Date","Name","Event","Review"\n`);
  }
  fs.appendFileSync(CSV_FILE, csvRow, "utf8");
}

// Submit Review API
app.post("/submit-review", async (req, res) => {
  const { name, event, reviewText } = req.body;
  if (!name || !event || !reviewText) {
    return res.status(400).json({ error: "All fields are required" });
  }

  const review = {
    name,
    event,
    reviewText,
    date: new Date().toISOString(),
  };

  try {
    const newFeedback = new Feedback(review);
    await newFeedback.save();
    writeToCSV(review);
    res.json({ message: "Review saved successfully" });
  } catch (err) {
    res.status(500).json({ error: "Failed to save review" });
  }
});

// Get All Reviews
app.get("/get-reviews", async (req, res) => {
  try {
    const reviews = await Feedback.find().sort({ date: -1 });
    res.json(reviews);
  } catch (err) {
    res.status(500).json({ error: "Failed to fetch reviews" });
  }
});

// Download CSV
app.get("/download-reviews", (req, res) => {
  if (!fs.existsSync(CSV_FILE)) {
    return res.status(404).send("No reviews available");
  }
  res.download(CSV_FILE, "event-reviews.csv");
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
