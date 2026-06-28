function UploadPanel({
  files,
  setFiles,
  rankCandidates,
  loading,
  selectedJobTitle,
}) {
  return (
    <div className="bg-white rounded-xl shadow p-6 h-full">

      <div className="flex justify-between items-center mb-5">

        <h2 className="text-xl font-bold">
          Upload Resumes
        </h2>

        {selectedJobTitle && (
          <span className="bg-blue-100 text-blue-700 text-sm font-semibold px-3 py-1 rounded-full">
            🤖 {selectedJobTitle}
          </span>
        )}

      </div>

      <label className="flex flex-col items-center justify-center h-56 border-2 border-dashed border-gray-300 rounded-xl cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition">

        <div className="text-6xl">
          📄
        </div>

        <p className="font-semibold mt-4">
          Drag & Drop resumes here
        </p>

        <p className="text-gray-500 text-sm mt-2">
          or click to browse PDF files
        </p>

        <p className="text-xs text-gray-400 mt-3">
          Multiple PDF resumes supported
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

      <div className="mt-6">

        <div className="flex justify-between items-center mb-3">

          <h3 className="font-semibold">
            Selected Resumes
          </h3>

          <span className="text-sm text-gray-500">
            {files.length} File{files.length !== 1 ? "s" : ""}
          </span>

        </div>

        <div className="max-h-48 overflow-y-auto space-y-2">

          {files.length === 0 ? (

            <div className="border rounded-lg p-4 text-center text-gray-400">
              No resumes selected
            </div>

          ) : (

            files.map((file) => (

              <div
                key={file.name}
                className="flex justify-between items-center border rounded-xl px-4 py-3 hover:bg-gray-50"
              >

                <div className="flex items-center gap-3">

                  <div className="text-2xl">
                    📄
                  </div>

                  <div>

                    <div className="font-medium truncate max-w-[180px]">
                      {file.name}
                    </div>

                    <div className="text-xs text-gray-500">
                      {(file.size / 1024).toFixed(1)} KB
                    </div>

                  </div>

                </div>

                <div className="text-green-600 font-semibold">
                  Ready
                </div>

              </div>

            ))

          )}

        </div>

      </div>

      <button
        onClick={rankCandidates}
        disabled={loading}
        className="mt-6 w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white rounded-xl py-3 font-semibold transition"
      >
        {loading
          ? "🤖 Analyzing Candidates..."
          : "🚀 Rank Candidates"}
      </button>

    </div>
  );
}

export default UploadPanel;