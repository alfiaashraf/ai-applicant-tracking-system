import { useMemo, useState } from "react";
import CandidateCard from "./CandidateCard";

function RankingPanel({ rankings }) {
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState("highest");

  const filteredRankings = useMemo(() => {
    let data = [...rankings];

    data = data.filter((candidate) =>
      candidate.filename.toLowerCase().includes(search.toLowerCase())
    );

    switch (sortBy) {
      case "highest":
        data.sort((a, b) => b.score - a.score);
        break;
      case "lowest":
        data.sort((a, b) => a.score - b.score);
        break;
      case "strong":
        data = data.filter(c => c.recommendation === "Strong");
        break;
      case "moderate":
        data = data.filter(c => c.recommendation === "Moderate");
        break;
      case "weak":
        data = data.filter(c => c.recommendation === "Weak");
        break;
      default:
        break;
    }

    return data;
  }, [rankings, search, sortBy]);

  const topCandidate =
    rankings.length > 0
      ? [...rankings].sort((a, b) => b.score - a.score)[0]
      : null;

  const averageScore =
    rankings.length === 0
      ? 0
      : rankings.reduce((sum, c) => sum + c.score, 0) / rankings.length;

  function exportCSV() {
    if (!filteredRankings.length) return;

    const rows = [
      [
        "Rank",
        "Filename",
        "Score",
        "Recommendation",
        "Matched Skills",
        "Missing Skills",
      ],
      ...filteredRankings.map((c, i) => [
        i + 1,
        c.filename,
        (c.score * 100).toFixed(2),
        c.recommendation,
        c.matched_skills.join(", "),
        c.missing_skills.join(", "),
      ]),
    ];

    const csv = rows.map(r => r.join(",")).join("\n");

    const blob = new Blob([csv], {
      type: "text/csv",
    });

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "candidate_rankings.csv";
    a.click();

    URL.revokeObjectURL(url);
  }

  return (
    <div className="bg-white rounded-xl shadow p-6">

      <div className="flex justify-between items-center">

        <h2 className="text-2xl font-bold">
          Candidate Rankings
        </h2>

        <button
          onClick={exportCSV}
          className="bg-indigo-600 text-white rounded-lg px-4 py-2"
        >
          Export CSV
        </button>

      </div>

      {topCandidate && (

        <div className="bg-yellow-50 border border-yellow-300 rounded-xl p-4 mt-5">

          <div className="text-xs text-yellow-700 font-bold">
            ⭐ TOP CANDIDATE
          </div>

          <div className="text-lg font-semibold mt-1">
            {topCandidate.filename}
          </div>

          <div className="mt-2">
            {(topCandidate.score * 100).toFixed(1)}%
          </div>

        </div>

      )}

      <div className="grid grid-cols-2 gap-3 mt-5">

        <div className="bg-blue-50 rounded-xl p-3">
          <div className="text-gray-500 text-sm">
            Candidates
          </div>

          <div className="text-2xl font-bold">
            {rankings.length}
          </div>
        </div>

        <div className="bg-green-50 rounded-xl p-3">
          <div className="text-gray-500 text-sm">
            Average Score
          </div>

          <div className="text-2xl font-bold">
            {(averageScore * 100).toFixed(1)}%
          </div>
        </div>

      </div>

      <input
        className="border rounded-lg p-3 w-full mt-5"
        placeholder="Search candidates..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <select
        className="border rounded-lg p-3 w-full mt-3 mb-5"
        value={sortBy}
        onChange={(e) => setSortBy(e.target.value)}
      >
        <option value="highest">Highest Score</option>
        <option value="lowest">Lowest Score</option>
        <option value="strong">Strong Only</option>
        <option value="moderate">Moderate Only</option>
        <option value="weak">Weak Only</option>
      </select>

      <div className="space-y-5 max-h-[450px] overflow-y-auto">

        {filteredRankings.map((candidate, index) => (
          <CandidateCard
            key={candidate.filename}
            candidate={candidate}
            index={index}
          />
        ))}

      </div>

    </div>
  );
}

export default RankingPanel;