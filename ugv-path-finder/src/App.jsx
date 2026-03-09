import React, { useState, useEffect } from "react";

const GRID_SIZE = 70;

export default function App() {

  const [start, setStart] = useState("0,0");
  const [goal, setGoal] = useState("69,69");

  const [density, setDensity] = useState(0.25);

  const [grid, setGrid] = useState([]);
  const [path, setPath] = useState([]);
  const [botIndex, setBotIndex] = useState(-1);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchGrid();
  }, []);

  const fetchGrid = async () => {
    try {
      const res = await fetch("http://localhost:8000/grid");
      const data = await res.json();

      if (Array.isArray(data.grid)) {
        setGrid(data.grid);
      } else {
        setGrid([]);
      }

    } catch (err) {
      console.error("Grid fetch failed:", err);
      setGrid([]);
    }
  };

  const reset = () => {
    setPath([]);
    setBotIndex(-1);
  };

  const startBotAnimation = (pathData) => {

    let i = 0;

    const interval = setInterval(() => {

      setBotIndex(i);
      i++;

      if (i >= pathData.length) {
        clearInterval(interval);
      }

    }, 30);
  };

  const computePath = async () => {

    setLoading(true);

    try {

      const res = await fetch(
        `http://localhost:8000/astar?start=${start}&goal=${goal}`
      );

      const data = await res.json();

      if (data.path) {
        setPath(data.path);
        startBotAnimation(data.path);
      }

    } catch (err) {
      console.error("A* failed:", err);
    }

    setLoading(false);
  };

  const generateGrid = async () => {

    try {

      await fetch(
        `http://localhost:8000/set-density?value=${Number(density)}`,
        { method: "POST" }
      );

      await fetch(
        "http://localhost:8000/generate-grid",
        { method: "POST" }
      );

      await fetchGrid();
      reset();

    } catch (err) {
      console.error("Grid generation failed:", err);
    }
  };

  const resetGrid = async () => {

    try {

      await fetch(
        "http://localhost:8000/generate-grid",
        { method: "POST" }
      );

      await fetchGrid();
      reset();

    } catch (err) {
      console.error("Grid reset failed:", err);
    }
  };

  const isPathCell = (row,col) =>
    path.some(p => p[0] === row && p[1] === col);

  const isBotCell = (row,col) => {
    if(botIndex < 0 || botIndex >= path.length) return false;
    const [x,y] = path[botIndex];
    return x === row && y === col;
  };

  return (

    <div className="app-wrapper">

      <div className="container">

        <h1 className="title">UGV Path Simulator</h1>
        <p className="subtitle">A* Battlefield Navigation</p>

        <div className="controls">

          <div className="input-group">
            <label>Start Node</label>
            <input
              value={start}
              onChange={(e)=>setStart(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label>Goal Node</label>
            <input
              value={goal}
              onChange={(e)=>setGoal(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label>Obstacle Density</label>
            <input
              type="number"
              step="0.05"
              min="0"
              max="1"
              value={density}
              onChange={(e)=>setDensity(Number(e.target.value))}
            />
          </div>

          <button
            className="compute-btn"
            onClick={generateGrid}
          >
            Generate Grid
          </button>

          <button
            className="compute-btn"
            onClick={resetGrid}
            style={{marginTop:"10px"}}
          >
            New Random Grid
          </button>

          <button
            className="compute-btn"
            onClick={computePath}
            disabled={loading}
            style={{marginTop:"10px"}}
          >
            {loading ? "Computing..." : "Start Navigation"}
          </button>

          <button
            className="compute-btn"
            onClick={reset}
            style={{marginTop:"10px"}}
          >
            Reset Path
          </button>

        </div>

        <div
          className="grid-container"
          style={{gridTemplateColumns:`repeat(${GRID_SIZE},8px)`}}
        >

          {Array.isArray(grid) && grid.length > 0 && grid.flatMap((row,rowIndex) =>
            row.map((cell,colIndex) => {

              let className = "grid-cell";

              if(cell === 1) className += " cell-obstacle";

              if(isPathCell(rowIndex,colIndex))
                className += " cell-path";

              if(isBotCell(rowIndex,colIndex))
                className += " cell-bot";

              if(start === `${rowIndex},${colIndex}`)
                className += " cell-start";

              if(goal === `${rowIndex},${colIndex}`)
                className += " cell-goal";

              return (
                <div
                  key={`${rowIndex}-${colIndex}`}
                  className={className}
                />
              );

            })
          )}

        </div>

        {path.length > 0 && (

          <div className="result">

            <div className="distance-number">
              {path.length}
              <span className="distance-unit">steps</span>
            </div>

            <div className="route-summary">
              {start} → {goal}
            </div>

            <div className="path-box">
              {JSON.stringify(path)}
            </div>

          </div>

        )}

      </div>

    </div>

  );
}