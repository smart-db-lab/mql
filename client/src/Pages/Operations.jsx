import { UploadOutlined } from "@ant-design/icons";
import { Button, Radio, Drawer, Spin } from "antd";
import TextArea from "antd/es/input/TextArea";
import Upload from "antd/es/upload/Upload";
import React, { useState } from "react";
import toast, { Toaster } from "react-hot-toast";
import { BiText } from "react-icons/bi";
import { FaRegFileAudio } from "react-icons/fa6";
import AudioInput from "../Components/AudioInput";
import ShowLog from "../Components/ShowLog";
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";
import CustomMonacoEditor from "../Components/CustomMonacoEditor";
import DefaultDataset from "../Components/DefaultDataset";
import { processQuery } from "../services/apiServices";

function Operations() {
  const [type, setType] = useState("text");
  const [audioTranscript, setAudioTranscript] = useState("");
  const [query, setQuery] = useState("");
  const [rowData, setRowData] = useState();
  const [fileList, setFileList] = useState([]);
  const [data, setData] = useState([]);
  const [showTestFile, setTestFile] = useState(false);
  const [testFileList, setTestFileList] = useState([]);
  const [isloding, setisloading] = useState(false);
  const [drawerVisible, setDrawerVisible] = useState(false);

  const handleExecute = async () => {
    setRowData();
    setisloading(true);
    setFileList([]);
    if (!query) {
      toast.error("Query can't be empty");
      setisloading(false);
      return;
    }
    let inputs = query.trim();
    if (inputs[inputs.length - 1] !== ";") {
      toast.error("Invalid Query.");
      setisloading(false);
      return;
    }
    inputs = inputs.split(";");
    inputs = inputs.slice(0, inputs.length - 1);
    inputs = inputs.map((val) => val.trim() + ";");
    for (let input of inputs) {
      if (!input) {
        toast.error("Invalid Query.");
        setisloading(false);
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

      const res = await processQuery(formData);
      let d = await res.json();
      setisloading(false);
      d = JSON.stringify(d).replaceAll("NaN", "null");
      d = JSON.parse(d);
      setData((prev) => [...prev, d]);
    } catch (error) {
      setisloading(false);
      toast.error(error.message || "Error executing query");
    }
  };

  return (
    <div className={`max-w-7xl mt-3 mx-auto`}>
      <Toaster />
      <div className="text-center">
        <Radio.Group
          // size="large"
          value={type}
          onChange={(e) => setType(e.target.value)}
          className="font-semibold"
          buttonStyle="solid"
        >
          <Radio.Button value={"text"} className="!font-secondary">
            <div className="flex items-center gap-2">
              <span className="">Query Editor</span>
              <span>
                <BiText size={18} />
              </span>
            </div>
          </Radio.Button>
          <Radio.Button value={"audio"} className="!font-secondary">
            <div className="flex items-center gap-2">
              <span>Audio Editor</span>
              <span>
                <FaRegFileAudio size={18} />
              </span>
            </div>
          </Radio.Button>
          <Radio.Button value={"nlp"} className="!font-secondary">
            <div className="flex items-center gap-2">
              <span>NLP Editor</span>
              <span>
                <FaRegFileAudio size={18} />
              </span>
            </div>
          </Radio.Button>
        </Radio.Group>
      </div>

      {type === "audio" && (
        <AudioInput
          audioTranscript={audioTranscript}
          setAudioTranscript={setAudioTranscript}
        />
      )}

      <div className="flex">
        {/* Drawer for Default Dataset */}
        <Drawer
          title="Default Dataset"
          placement="left"
          closable={true}
          onClose={() => setDrawerVisible(false)}
          open={drawerVisible}
          width={300}
        >
          <DefaultDataset />
        </Drawer>

        <PanelGroup
          key={type}
          direction="horizontal"
          className="flex-grow flex !flex-row gap-4"
        >
          {type === "nlp" && (
            <Panel defaultSize={25} minSize={20}>
              <div className="">
                <h1 className="text-lg font-semibold mt-5">Enter your query</h1>
                <TextArea size='large' className="h-52 " style={{ height: '200px' }}></TextArea>
                <button className="mt-4 bg-blue-500 rounded text-white p-2 px-4 font-secondary font-semibold">
                  Convert To DL
                </button>
              </div>
            </Panel>
          )}
          {type === "text" && (
            <Panel defaultSize={25} minSize={20}>
              <div className="mt-2 flex flex-col bg-white z-50 py-4 overflow-y-auto">
                <h1 className=" font-secondary text-lg font-semibold mb-4">
                  Enter your query
                </h1>
                <div className="border rounded box-border border-slate-400">
                  <CustomMonacoEditor
                    query={query}
                    setQuery={setQuery}
                    setTestFile={setTestFile}
                  />
                </div>
                <div className="mt-4">
                  <Upload
                    className="!text-lg"
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
                  <button
                    onClick={() => setDrawerVisible(true)}
                    className="mt-4 w-28 text-sm border-slate-400 border rounded-lg text-black p-1  shadow-lg  hover:bg-slate-100 hover:shadow-lg"
                  >
                    Default Dataset
                  </button>
                </div>
                {showTestFile && (
                  <div className="mt-4">
                    <Upload
                      className="!text-lg"
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
                <h1 className="text-lg font-semibold mt-3">
                  Click on Execute QueryButton to MQL Query Processor To Generate Output
                </h1>
                <button
                  className="mt-4 w-38 ml-auto text-lg bg-blue-500 rounded-lg text-white p-1 px-2 font-bold font-secondary shadow-lg hover:bg-blue-900 hover:shadow-lg"
                  onClick={handleExecute}
                >
                  Execute Query
                </button>
              </div>
            </Panel>
          )}
          <PanelResizeHandle className="border border-dotted border-gray-300" />
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
