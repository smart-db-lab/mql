import { UploadOutlined } from "@ant-design/icons";
import { Button, Radio ,Spin} from "antd";
import TextArea from "antd/es/input/TextArea";
import Upload from "antd/es/upload/Upload";
import React, { useState } from "react";
import toast, { Toaster } from "react-hot-toast";
import { BiText } from "react-icons/bi";
import { FaRegFileAudio } from "react-icons/fa6";
import AudioInput from "../Components/AudioInput";
import ShowLog from "../Components/ShowLog";
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";

/*
CREATE ESTIMATOR salaryPredictor TYPE LR FORMULA $salary~years$;
CREATE TRAINING PROFILE oneshotSalary WITH [SELECT * FROM salary];
USE 'data/salarydb.db';
TRAIN salaryPredictor WITH TRAINING PROFILE oneshotSalary;
PREDICT WITH TRAINING PROFILE oneshotSalary BY ESTIMATOR salaryPredictor;
*/

function Operations() {
  const [type, setType] = useState("text");
  const [audioTranscript, setAudioTranscript] = useState("");
  const [query, setQuery] = useState("");
  const [rowData, setRowData] = useState();
  const [fileList, setFileList] = useState([]);
  const [data, setData] = useState([]);
  const [showTestFile, setTestFile] = useState(false);
  const [testFileList, setTestFileList] = useState([]);
  const [isloding,setisloading] =useState(false)
  const handleExecute = async () => {
    setRowData();
    setisloading(true)
    if (!query) {
      toast.error("Query can't be empty");
      return;
    }
    let inputs = query.trim();
    if (inputs[inputs.length - 1] !== ";") {
      toast.error("Invalid Query.");
      return;
    }
    inputs = inputs.split(";");
    inputs = inputs.slice(0, inputs.length - 1);
    inputs = inputs.map((val) => val.trim() + ";");
    for (let input of inputs) {
      if (!input) {
        toast.error("Invalid Query.");
        return;
      }
    }
    try {
      const formData = new FormData();
      formData.append("input", inputs);
      if (fileList && fileList[0] && fileList[0].originFileObj)
        formData.append("file", fileList[0].originFileObj);
      if (testFileList && testFileList[0] && testFileList[0].originFileObj)
        formData.append("test", testFileList[0].originFileObj);

      const res = await fetch("http://localhost:8000/test_url/", {
        method: "POST",
        body: formData,
      });
      let d = await res.json();
      setisloading(false)
      d = d.replaceAll("NaN", "null");

      console.log(d);
      d = JSON.parse(d);

      setData((prev) => [...prev, d]);
    } catch (error) {
      setisloading(false)
      console.log(error);
    }
  };

  return (
    <div className={` max-w-7xl mx-auto`}>
      <Toaster />
      {/* {type === "audio" && (
        <AudioInput
          audioTranscript={audioTranscript}
          setAudioTranscript={setAudioTranscript}
        />
      )} */}
      <div className="">
        <PanelGroup direction="horizontal" className="flex !flex-row gap-4">
          <Panel defaultSize={25} minSize={20}>
            <div className="mt-2 flex flex-col  bg-white z-50 py-4 overflow-y-auto">
              <h1 className="text-center font-secondary text-2xl font-semibold mb-4 ">
                Enter your query
              </h1>
              <TextArea
                value={query}
                onChange={(e) => {
                  setQuery(e.target.value);
                  let q = e.target.value.toLowerCase().includes(" over ");
                  setTestFile(q);
                }}
                rows={8}
                placeholder="Enter your SQL query"
                className="font-secondary text-gray-800 text-lg"
              />
              <div className="mt-4">
                <Upload
                  className="!text-2xl"
                  fileList={fileList.map((file) => ({
                    ...file,
                    status: "done",
                  }))}
                  beforeUpload={(file) => {
                    setFileList([
                      { uid: file.uid, name: file.name, status: "done" },
                    ]);
                    return false;
                  }}
                  onChange={(e) => setFileList(e.fileList)}
                >
                  {fileList.length === 0 && (
                    <Button icon={<UploadOutlined />}>Upload File</Button>
                  )}
                </Upload>
              </div>
              {showTestFile && (
                <div className="mt-4">
                  <Upload
                    className="!text-2xl"
                    fileList={testFileList.map((file) => ({
                      ...file,
                      status: "done",
                    }))}
                    beforeUpload={(file) => {
                      setTestFileList([
                        { uid: file.uid, name: file.name, status: "done" },
                      ]);
                      return false;
                    }}
                    onChange={(e) => setTestFileList(e.fileList)}
                  >
                    {testFileList.length === 0 && (
                      <Button icon={<UploadOutlined />}>
                        Upload Test File
                      </Button>
                    )}
                  </Upload>
                </div>
              )}
              <button
                className="mt-4 w-28 ml-auto text-xl bg-blue-500 rounded-lg text-white p-2 px-4 font-secondary shadow-lg font-semibold hover:bg-blue-900 hover:shadow-lg"
                onClick={handleExecute}
              >
                Execute
              </button>
            </div>
          </Panel>
          <PanelResizeHandle  className="border border-dotted border-gray-300" />
          <Panel defaultSize={30} minSize={50}>
            <div className="relative top-8 pb-8 overflow-y-auto">
              <ShowLog data={data} setData={setData} isloding={isloding} />
            </div>
          </Panel>
        </PanelGroup>
      </div>
    </div>
  );
}

export default Operations;

/*

*/
