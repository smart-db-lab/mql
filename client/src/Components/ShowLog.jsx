import React, { useContext } from "react";
import { FaAnglesRight } from "react-icons/fa6";
import AgGridTable from "../Components/AgGridTable";
import { Collapse, Spin, Dropdown, Menu, Button } from "antd";
import { IoIosArrowForward } from "react-icons/io";
import Papa from "papaparse";
import { downloadCSV, downloadGraph, downloadFile, downloadPDF } from "../utility/download";
import PerformanceTable from "./PerformanceTable";
import { ThemeContext } from "../utility/ThemeContext";

// Custom hook for theme context with fallback
const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    console.warn('useTheme must be used within a ThemeProvider. Using default light mode.');
    return { darkMode: false, setDarkMode: () => {} };
  }
  return context;
};

function ShowLog({ data = [], setData, isloding }) {
  const { darkMode } = useTheme();
  // console.log('ShowLog re-rendered with darkMode:', darkMode); // Debug log
  const API_BASE = import.meta.env.VITE_BACKEND_URL|| "http://localhost:8000";
  return (
    <>
      <h1 className={`font-secondary flex justify-between text-lg font-semibold ${darkMode ? 'text-white' : 'text-black'}`}>
        <div className="flex">
          <span className="text-md">Output</span>
          <div className="m-2 flex">{isloding && <Spin />}</div>
        </div>
        {data.length > 0 && (
          <button
            className={`text-md bg-blue-500 hover:bg-red-600 w-20 py-1 text-white font-semibold rounded-md shadow-md transition-colors ${darkMode ? 'darkmode' : ' '}`}
            onClick={() => setData([])}
          >
            Clear
          </button>
        )}
      </h1>
      {data.length > 0 ? (
        <div
          className={`mt-2 space-y-4 ${darkMode ? 'bg-gray-700' : 'bg-gray-100'} shadow-md p-3 py-5 overflow-y-auto rounded-lg`}
          style={{ maxHeight: "calc(100vh - 250px)" }}
        >
          {data.map((val, key) => (
            <Collapse
              key={key}
              className={`flex items-start gap-3 !w-full ${darkMode ? 'dark-collapse' : ''}`}
              items={[
                {
                  key,
                  label: (
                    <div className={`flex justify-between items-center ${darkMode ? 'text-white' : 'text-black'}`}>
                      <p className={`font-medium text-lg ${darkMode ? 'text-white' : 'text-black'}`}>Output - {key + 1}</p>
                      <Button
                        type="primary"
                        size="small"
                        className={`ml-2 bg-slate-400 hover:bg-slate-600 border-slate-300 ${darkMode ? 'darkmode' : ' '}`}
                        onClick={(e) => {
                          e.stopPropagation();
                          downloadPDF(`output-${key}`, `output-${key + 1}-report.pdf`, val);
                        }}
                      >
                        📄 Download PDF
                      </Button>
                    </div>
                  ),
                  className: "w-full",
                  children: (
                    <div id={`output-${key}`} className={`space-y-6 !w-full bg-transparent ${darkMode ? 'text-white' : 'text-black'}`}>
                      {Object.keys(val).map((v, ind) => (
                        <div key={ind} className={`p-3 rounded-lg ${darkMode ? 'bg-gray-800' : 'bg-white'} shadow-md`}>
                          {console.log("here table ", val[v])}

                          {/* {val[v]["text"] && (
                            <div className="font-secondary text-lg text-gray-800 font-semibold relative -top-2">
                              {val[v]["text"].map((item, index) => (
                                <div key={index}>
                                  {typeof item === "object" &&
                                  !Array.isArray(item) ? (
                                    <>
                                      <div className="flex justify-between bg-gray-100 rounded-lg px-2">
                                        <div className="m-1 p-1">
                                          {Object.entries(item)
                                            .slice(0, 1)
                                            .map(([key, value]) => (
                                              <p className="flex" key={key}>
                                                {key}: {value}
                                              </p>
                                            ))}
                                        </div>
                                        <Dropdown
                                          className="inline-block font"
                                          overlay={
                                            <Menu>
                                              {Object.entries(item)
                                                .slice(1)
                                                .map(([key, value], idx) => (
                                                  <Menu.Item key={idx}>
                                                    {key}: {value}
                                                  </Menu.Item>
                                                ))}
                                            </Menu>
                                          }
                                          trigger={["click"]}
                                        >
                                          <div className="cursor-pointer inline-block">
                                            <IoIosArrowForward className="inline-block mt-2" />
                                          </div>
                                        </Dropdown>
                                      </div>
                                    </>
                                  ) : (
                                    <p>{item}</p>
                                  )}
                                </div>
                              ))}

                            </div>
                          )} */}
                          {/* <div className="pt-5 gap-2"></div> */}
                          {val[v]["query"] && (
                            <>
                              <h1 className={`font-semibold ${darkMode ? 'text-white' : 'text-black'}`}>Query :</h1>
                              <p className={`${darkMode ? 'bg-gray-600 text-white' : 'bg-slate-100 text-black'} p-2 font-secondary m-2 rounded`}>
                                {val[v]["query"]}</p>
                            </>
                          )}
                          {val[v]["text"] && (
                            <>
                              <h1 className={`font-semibold ${darkMode ? 'text-white' : 'text-black'}`}>Log :</h1>
                              <div className={`${darkMode ? 'text-gray-200' : 'text-black'}`}>
                                {Array.isArray(val[v]["text"])
                                  ? val[v]["text"].map((item, idx) => (
                                    <div key={idx}>{item}</div>
                                  ))
                                  : val[v]["text"]}
                              </div>
                            </>
                          )}
                          {val[v]["performance_table"] && (
                            <>
                              <h1 className={`font-semibold ${darkMode ? 'text-white' : 'text-black'}`}>AutoML Evaluation :</h1>
                              <PerformanceTable
                                rowData={val[v]["performance_table"]}
                              />
                            </>
                          )}
                          <div className="pt-5 "></div>
                          {val[v]["table"] && val[v]["table"].length > 0 && (
                            <>
                              <h1 className={`font-semibold ${darkMode ? 'text-white' : 'text-black'}`}>Data Table :</h1>
                              <AgGridTable rowData={val[v]["table"]} />
                              <Button
                                type="primary"
                                className="mt-2 bg-blue-500 hover:bg-blue-600"
                                onClick={() =>
                                  downloadCSV(
                                    val[v]["table"],
                                    `output-${key + 1}.csv`
                                  )
                                }
                              >
                                Download CSV
                              </Button>
                            </>
                          )}
                          {val[v]?.['graph_link']?.graph_jpg && (
                            <>
                              {/* {console.log(val[v]['graph_link'])} */}
                              {/* <img
                                src={`data:image/png;base64,${val[v]['graph']}`}
                                alt="Graph"
                              /> */}
                              {/* {console.log(`${API_BASE}${val[v]['graph_link'].graph_jpg}`)} */}
                                <img
                                  src={`${API_BASE}${val[v]['graph_link'].graph_jpg}`}
                                  alt="Graph"
                                  className="rounded-md border border-gray-300 shadow-md max-w-full"
                                />
                              <Dropdown
                                overlay={
                                  <Menu>
                                    <Menu.Item
                                      key="1"
                                      onClick={() =>
                                        downloadFile(val[v]['graph_link'].graph_png, "graph.png")
                                      }
                                    >
                                      Download as PNG
                                    </Menu.Item>
                                    <Menu.Item
                                      key="2"
                                      onClick={() =>
                                        downloadFile(val[v]['graph_link'].graph_svg, "graph.svg")
                                      }
                                    >
                                      Download as SVG
                                    </Menu.Item>
                                    <Menu.Item
                                      key="3"
                                      onClick={() =>

                                        downloadFile(val[v]['graph_link'].graph_jpg, "graph.jpg")
                                      }
                                    >
                                      Download as JPG
                                    </Menu.Item>
                                  </Menu>
                                }
                              >
                                <Button className="mt-2 text-white bg-blue-500 hover:bg-blue-600">
                                  Download Graph
                                </Button>
                              </Dropdown>
                            </>
                          )}
                        </div>
                      ))}
                    </div>
                  ),
                },
              ]}
            ></Collapse>
          ))}
        </div>
      ) : (
        <div className={`${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50 text-black'} rounded mt-2 p-3 py-7 text-center font-medium text-md transition-colors`}>
          <p>Run a query to see the output</p>
        </div>
      )}
    </>
  );
}

export default ShowLog;
