function JobPanel({
  jobTitle,
  setJobTitle,
  jobDescription,
  setJobDescription,
  saveJob,
  jobId,
  jobs,
  selectedJobId,
  setSelectedJobId,
}) {
  return (
    <div className="bg-white rounded-xl shadow p-6 h-full">

      <h2 className="text-xl font-bold mb-5">
        Create Job
      </h2>

      <input
        type="text"
        placeholder="Job Title"
        value={jobTitle}
        onChange={(e) => setJobTitle(e.target.value)}
        className="border rounded-xl w-full p-3 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <textarea
        className="border rounded-xl w-full h-60 p-4 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Paste the complete job description here..."
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
      />

      <button
        onClick={saveJob}
        className="mt-5 w-full bg-blue-600 hover:bg-blue-700 text-white rounded-xl py-3 font-semibold transition"
      >
        Save Job
      </button>

      {jobId && (
        <div className="mt-5 rounded-lg bg-green-50 border border-green-200 p-3">

          <p className="text-green-700 font-medium">
            ✅ Job Created Successfully
          </p>

          <p className="text-xs break-all text-gray-600 mt-2">
            {jobId}
          </p>

        </div>
      )}

      <hr className="my-6" />

      <h3 className="font-semibold mb-3">
        Saved Jobs
      </h3>

      <div className="space-y-2 max-h-64 overflow-y-auto">

        {jobs.length === 0 ? (

          <p className="text-gray-400 text-sm">
            No jobs created yet.
          </p>

        ) : (

          jobs.map((job) => (

            <button
              key={job.id}
              onClick={() => setSelectedJobId(job.id)}
              className={`w-full rounded-lg border p-3 text-left transition ${
                selectedJobId === job.id
                  ? "border-blue-600 bg-blue-50"
                  : "hover:bg-gray-50"
              }`}
            >

              <div className="font-semibold">
                {job.title}
              </div>

              <div className="text-xs text-gray-500 mt-1">
                {new Date(job.created_at).toLocaleString()}
              </div>

            </button>

          ))

        )}

      </div>

    </div>
  );
}

export default JobPanel;