import Papa from "papaparse";

export const downloadCSV = (tableData, fileName) => {
  const csv = Papa.unparse(tableData);
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.setAttribute("download", fileName);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};


export const downloadGraph = (graphData, fileName) => {
const link = document.createElement('a');
link.href = `data:image/png;base64,${graphData}`;
link.setAttribute('download', fileName);
document.body.appendChild(link);
link.click();
document.body.removeChild(link);
}
