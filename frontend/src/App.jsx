import { useEffect, useState } from "react";
import api from "./services/api";

import JobPanel from "./components/JobPanel";
import UploadPanel from "./components/UploadPanel";
import RankingPanel from "./components/RankingPanel";

function App() {
  const [jobDescription, setJobDescription] = useState("");
  const [jobId, setJobId] = useState("");
  const [files, setFiles] = useState([]);
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [jobs, setJobs] = useState([]);
  const [selectedJobId, setSelectedJobId] = useState("");
  const [jobTitle, setJobTitle] = useState("");

  useEffect(() => {
    loadJobs();
  }, []);

  async function loadJobs() {
    try {
      const response = await api.get("/jobs");

      setJobs(response.data);

      if (response.data.length > 0) {
        setSelectedJobId(response.data[0].id);
      }
    } catch (error) {
      console.error(error);
    }
  }

  async function saveJob() {
    try {
      const response = await api.post("/jobs", {
        title: jobTitle,
        description: jobDescription,
      });

      await loadJobs();

      setJobId(response.data.id);
      setSelectedJobId(response.data.id);

      alert("Job Created Successfully!");
    } catch (error) {
      console.error(error);

      setJobTitle("");
      setJobDescription("");

      if (error.response) {
        alert(error.response.data.detail || "Backend Error");
      } else {
        alert("Cannot connect to FastAPI server.");
      }
    }
  }

  async function rankCandidates() {
    if (!selectedJobId) {
      alert("Select a job first.");
      return;
    }

    if (files.length === 0) {
      alert("Upload at least one resume.");
      return;
    }

    try {
      setLoading(true);

      const formData = new FormData();

      formData.append("job_id", selectedJobId);

      files.forEach((file) => {
        formData.append("files", file);
      });

      const response = await api.post(
        "/ranking/rank",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setRankings(response.data.rankings);
    } catch (error) {
      console.error(error);

      if (error.response) {
        alert(error.response.data.detail || "Ranking failed");
      } else {
        alert("Cannot connect to FastAPI server.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-100">

      <div className="max-w-7xl mx-auto px-8 py-10">

        <div className="mb-10">

          <h1 className="text-5xl font-bold text-slate-800">
            AI Applicant Tracking System
          </h1>

          <p className="text-slate-500 mt-2 text-lg">
            Recruiter Dashboard
          </p>

        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

        <JobPanel
          jobTitle={jobTitle}
          setJobTitle={setJobTitle}
          jobDescription={jobDescription}
          setJobDescription={setJobDescription}
          saveJob={saveJob}
          jobId={jobId}
          jobs={jobs}
          selectedJobId={selectedJobId}
          setSelectedJobId={setSelectedJobId}
        />

        <UploadPanel
          files={files}
          setFiles={setFiles}
          rankCandidates={rankCandidates}
          loading={loading}
          selectedJobTitle={
            jobs.find((job) => job.id === selectedJobId)?.title
          }
        />

          <RankingPanel
            rankings={rankings}
          />

        </div>

      </div>

    </div>
  );
}

export default App;