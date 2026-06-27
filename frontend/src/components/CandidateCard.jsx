function CandidateCard({ candidate, index }) {
    const percentage = (candidate.score * 100).toFixed(1);
  
    const badge =
      candidate.recommendation === "Strong"
        ? "bg-green-100 text-green-700"
        : candidate.recommendation === "Moderate"
        ? "bg-yellow-100 text-yellow-700"
        : "bg-red-100 text-red-700";
  
    const explanation = [];
  
    if (candidate.matched_skills.length >= 5) {
      explanation.push(
        `Strong skills match (${candidate.matched_skills.length} skills)`
      );
    } else if (candidate.matched_skills.length > 0) {
      explanation.push(
        `${candidate.matched_skills.length} relevant skill${
          candidate.matched_skills.length > 1 ? "s" : ""
        } matched`
      );
    }
  
    if (candidate.missing_skills.length === 0) {
      explanation.push("No important skills missing");
    } else if (candidate.missing_skills.length <= 2) {
      explanation.push(
        `Only ${candidate.missing_skills.length} skill gap${
          candidate.missing_skills.length > 1 ? "s" : ""
        }`
      );
    } else {
      explanation.push(
        `${candidate.missing_skills.length} important skills missing`
      );
    }
  
    return (
      <div className="bg-white border rounded-2xl p-5 shadow-sm hover:shadow-xl transition">
  
        <div className="flex justify-between items-start">
  
          <div>
  
            <div className="text-sm text-gray-400">
              Candidate #{index + 1}
            </div>
  
            <h3 className="font-semibold text-lg break-all mt-1">
              {candidate.filename}
            </h3>
  
          </div>
  
          <span
            className={`px-3 py-1 rounded-full text-sm font-semibold ${badge}`}
          >
            {candidate.recommendation}
          </span>
  
        </div>
  
        <div className="mt-6">
  
          <div className="flex justify-between mb-2">
  
            <span className="font-medium">
              Overall Match
            </span>
  
            <span className="font-bold text-lg">
              {percentage}%
            </span>
  
          </div>
  
          <div className="w-full bg-gray-200 rounded-full h-3">
  
            <div
              className="bg-gradient-to-r from-blue-500 to-indigo-600 h-3 rounded-full"
              style={{
                width: `${percentage}%`,
              }}
            />
  
          </div>
  
        </div>
  
        <div className="mt-6 rounded-xl bg-slate-50 p-4">
  
          <div className="font-semibold text-slate-700 mb-2">
            AI Explanation
          </div>
  
          <ul className="space-y-2 text-sm">
  
            {explanation.map((item) => (
              <li key={item}>
                ✅ {item}
              </li>
            ))}
  
          </ul>
  
        </div>
  
        <div className="mt-6">
  
          <div className="font-semibold text-green-700 mb-2">
            Matched Skills
          </div>
  
          <div className="flex flex-wrap gap-2">
  
            {candidate.matched_skills.length ? (
              candidate.matched_skills.map((skill) => (
                <span
                  key={skill}
                  className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-medium"
                >
                  {skill}
                </span>
              ))
            ) : (
              <span className="text-gray-400">
                None
              </span>
            )}
  
          </div>
  
        </div>
  
        <div className="mt-5">
  
          <div className="font-semibold text-red-600 mb-2">
            Missing Skills
          </div>
  
          <div className="flex flex-wrap gap-2">
  
            {candidate.missing_skills.length ? (
              candidate.missing_skills.map((skill) => (
                <span
                  key={skill}
                  className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-xs font-medium"
                >
                  {skill}
                </span>
              ))
            ) : (
              <span className="text-gray-400">
                None
              </span>
            )}
  
          </div>
  
        </div>
  
      </div>
    );
  }
  
  export default CandidateCard;