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


// export const downloadGraph = (graphData, fileName) => {
// const link = document.createElement('a');
// link.href = graphData
// link.setAttribute('download', fileName);
// document.body.appendChild(link);
// link.click();
// document.body.removeChild(link);
// }

export const downloadGraph = (graphUrl, fileName) => {
  const link = document.createElement('a');
  link.href = graphUrl; 
  link.setAttribute('download', fileName);
  // link.href = `data:image/png;base64,${graphData}`;
  // link.setAttribute('target', '_blank');  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};


export const downloadFile = async (url, filename) => {
  try {
    const response = await fetch(`http://localhost:8000${url}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const blob = await response.blob(); 
    const downloadUrl = window.URL.createObjectURL(blob); 

    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = filename; 
    document.body.appendChild(a); 
    a.click(); 
    a.remove(); 
    window.URL.revokeObjectURL(downloadUrl);
  } catch (error) {
    console.error('Error downloading the file:', error);
  }
};
