const mongoose = require("mongoose");
const fs = require("fs");
const { Parser } = require("json2csv");
const axios = require("axios");
const FormData = require("form-data");

// ✅ Fill these with your values
const MONGO_URI = "mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority";
const ML_ENDPOINT = "http://127.0.0.1:8000/analyze"; // FastAPI backend endpoint

mongoose.connect(MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

const commentSchema = new mongoose.Schema({}, { strict: false });
const Comment = mongoose.model("Comment", commentSchema);

const exportAndSend = async () => {
  try {
    const comments = await Comment.find({});
    const jsonComments = comments.map(c => c.toObject());

    // ✅ Generate CSV
    const parser = new Parser({
      fields: ["username", "message", "sentiment", "confidence", "timestamp"]
    });
    const csv = parser.parse(jsonComments);
    const csvPath = "comments-latest.csv";
    fs.writeFileSync(csvPath, csv);

    // 📤 Send CSV as multipart/form-data
    const form = new FormData();
    form.append("file", fs.createReadStream(csvPath));

    const response = await axios.post(ML_ENDPOINT, form, {
      headers: form.getHeaders()
    });

    console.log("✅ CSV file sent at", new Date().toLocaleTimeString());
    console.log("🧠 ML Response:", response.data);

  } catch (err) {
    console.error("❌ Error sending to ML backend:", err.message);
  }
};

// 🔁 Run every 30 seconds
setInterval(exportAndSend, 30000);
console.log("🚀 Sending MongoDB → FastAPI every 30s...");
