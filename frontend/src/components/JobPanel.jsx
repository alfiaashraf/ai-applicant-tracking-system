function JobPanel({
    jobDescription,
    setJobDescription,
    saveJob,
    jobId,
  }) {
    return (
      <div className="bg-white rounded-xl shadow p-6 h-full">
  
        <h2 className="text-xl font-bold mb-5">
          Create Job
        </h2>
  
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
  
      </div>
    );
  }
  
  export default JobPanel;