function UploadPanel({
    files,
    setFiles,
    rankCandidates,
    loading,
  }) {
    return (
      <div className="bg-white rounded-xl shadow p-6 h-full">
  
        <h2 className="text-xl font-bold mb-5">
          Upload Resumes
        </h2>
  
        <label className="flex flex-col items-center justify-center h-52 border-2 border-dashed border-gray-300 rounded-xl cursor-pointer hover:bg-gray-50 transition">
  
          <div className="text-5xl mb-3">
            📄
          </div>
  
          <p className="font-medium">
            Click to choose PDF resumes
          </p>
  
          <p className="text-sm text-gray-500 mt-2">
            Hold Ctrl to select multiple files
          </p>
  
          <input
            type="file"
            accept=".pdf"
            multiple
            className="hidden"
            onChange={(e) =>
              setFiles(Array.from(e.target.files))
            }
          />
  
        </label>
  
        <div className="mt-5 max-h-40 overflow-y-auto">
  
          {files.length === 0 ? (
  
            <p className="text-gray-400 text-sm">
              No resumes selected.
            </p>
  
          ) : (
  
            files.map((file) => (
  
              <div
                key={file.name}
                className="flex justify-between items-center border rounded-lg px-3 py-2 mt-2"
              >
                <span className="truncate">
                  📄 {file.name}
                </span>
  
                <span className="text-xs text-gray-500">
                  {(file.size / 1024).toFixed(1)} KB
                </span>
  
              </div>
  
            ))
  
          )}
  
        </div>
  
        <button
          onClick={rankCandidates}
          disabled={loading}
          className="mt-6 w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white rounded-lg py-3 font-semibold transition"
        >
          {loading ? "Ranking Candidates..." : "Rank Candidates"}
        </button>
  
      </div>
    );
  }
  
  export default UploadPanel;