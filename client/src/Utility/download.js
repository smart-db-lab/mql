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
// // link.href = `data:image/png;base64,${graphData}`;
// link.href = graphData
// link.setAttribute('download', fileName);
// document.body.appendChild(link);
// link.click();
// document.body.removeChild(link);
// }

export const downloadGraph = (graphUrl, fileName) => {
  const link = document.createElement('a');
  link.href = graphUrl;  // Use the direct URL instead of base64
  link.setAttribute('download', fileName);
  // link.setAttribute('target', '_blank');  // Open in new tab
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};


export const downloadFile = async (url, filename) => {
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const blob = await response.blob(); // Convert the response to a blob
    const downloadUrl = window.URL.createObjectURL(blob); // Create a URL for the blob

    // Create an anchor element to download the file
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = filename; // Set the desired file name
    document.body.appendChild(a); // Append the anchor to the body
    a.click(); // Programmatically click the anchor to trigger the download
    a.remove(); // Remove the anchor from the body
    window.URL.revokeObjectURL(downloadUrl); // Free up memory
  } catch (error) {
    console.error('Error downloading the file:', error);
  }
};

// Example usage:
// downloadFile('/media/graph_a347abb9-2eef-41cf-9880-99c64a1a4371.jpg', 'downloaded_image.jpg');

