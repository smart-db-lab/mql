import React from "react";
import { FaAnglesRight } from "react-icons/fa6";
import AgGridTable from "../Components/AgGridTable";
import { Collapse, Spin, Dropdown, Menu, Button } from "antd";
import { IoIosArrowForward } from "react-icons/io";
import Papa from "papaparse";
import { downloadCSV, downloadGraph } from "../Utility/download";
function ShowLog({ data = [], setData, isloding }) {
  return (
    <>
      <h1 className="font-secondary flex justify-between text-2xl font-semibold">
        <div className="flex">
          <span className="text-md">Output</span>
          <div className="m-2 flex">{isloding && <Spin />}</div>
        </div>
        {data.length > 0 && (
          <button
            className="text-lg bg-blue-500 w-20 py-1 text-white font-semibold rounded-md shadow-md hover:bg-red-900 hover:shadow-lg"
            onClick={() => setData([])}
          >
            Clear
          </button>
        )}
      </h1>
      {data.length > 0 ? (
        <div
          className="mt-2 space-y-4 bg-gray-100 shadow-md p-3 py-5 overflow-y-auto rounded-lg"
          style={{ maxHeight: "calc(100vh - 250px)" }}
        >
          {data.map((val, key) => (
            <Collapse
              key={key}
              className="flex items-start gap-3 !w-full"
              items={[
                {
                  key,
                  label: (
                    <p className="font-medium text-lg">Output - {key + 1}</p>
                  ),
                  className: "w-full",
                  children: (
                    <div className="space-y-6 !w-full bg-transparent">
                      {Object.keys(val).map((v, ind) => (
                        <div key={ind}>
                          {val[v]["text"] && (
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
                          )}
                          {val[v]["table"] && val[v]["table"].length > 0 && (
                            <>
                              <AgGridTable rowData={val[v]["table"]} />
                              <Button
                                type="primary"
                                className="mt-2 bg-blue-500"
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
                          {val[v]["graph"] && (
                            <>
                              <img
                                src={`data:image/png;base64,${val[v]["graph"]}`}
                                alt="Graph"
                                onError={(e) => {
                                  e.target.src = "image doesn't load";
                                }}
                              />
                              <Button
                                type="primary"
                                className="mt-2 bg-blue-500"
                                onClick={() =>
                                  downloadGraph(
                                    val[v]["graph"],
                                    `graph-${key + 1}.png`
                                  )
                                }
                              >
                                Download Graph
                              </Button>
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
        <div className="bg-gray-100 shadow-md rounded mt-2 p-3 py-10 text-center font-medium text-xl">
          <p>Run a query to see the output</p>
        </div>
      )}
    </>
  );
}

export default ShowLog;
