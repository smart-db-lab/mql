import Papa from "papaparse";
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

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

export const downloadPDF = async (elementId, fileName, outputData) => {
  try {
    console.log('Starting PDF generation with data:', outputData);
    
    const element = document.getElementById(elementId);
    if (!element) {
      console.error('Element not found for PDF generation');
      return;
    }

    // Create a new jsPDF instance
    const pdf = new jsPDF('p', 'mm', 'a4');
    let yPosition = 20;

    // Add title
    pdf.setFontSize(16);
    pdf.text('ML Output Report', 20, yPosition);
    yPosition += 15;

    // Handle the case where outputData is the full val object with multiple keys
    const dataKeys = Object.keys(outputData);
    console.log('Data keys found:', dataKeys);

    // Process each key in the outputData
    for (let i = 0; i < dataKeys.length; i++) {
      const key = dataKeys[i];
      const currentData = outputData[key];
      
      if (!currentData || typeof currentData !== 'object') {
        continue;
      }

      // Add section header if there are multiple data sections
      if (dataKeys.length > 1) {
        if (yPosition > 260) {
          pdf.addPage();
          yPosition = 20;
        }
        pdf.setFontSize(14);
        pdf.text(`Section ${i + 1}`, 20, yPosition);
        yPosition += 10;
      }

      // Add query
      if (currentData.query) {
        console.log('Adding query to PDF');
        if (yPosition > 260) {
          pdf.addPage();
          yPosition = 20;
        }
        pdf.setFontSize(12);
        pdf.text('Query:', 20, yPosition);
        yPosition += 7;
        pdf.setFontSize(10);
        const queryLines = pdf.splitTextToSize(currentData.query, 170);
        pdf.text(queryLines, 20, yPosition);
        yPosition += queryLines.length * 5 + 10;
      }

      // Add text logs
      if (currentData.text && Array.isArray(currentData.text)) {
        console.log('Adding text logs to PDF');
        if (yPosition > 260) {
          pdf.addPage();
          yPosition = 20;
        }
        pdf.setFontSize(12);
        pdf.text('Logs:', 20, yPosition);
        yPosition += 7;
        pdf.setFontSize(10);
        
        currentData.text.forEach((text) => {
          const textLines = pdf.splitTextToSize(text, 170);
          if (yPosition + textLines.length * 5 > 280) {
            pdf.addPage();
            yPosition = 20;
          }
          pdf.text(textLines, 20, yPosition);
          yPosition += textLines.length * 5 + 5;
        });
      }

      // Add performance table
      if (currentData.performance_table && currentData.performance_table.length > 0) {
        console.log('Adding performance table to PDF:', currentData.performance_table);
        if (yPosition + 40 > 280) {
          pdf.addPage();
          yPosition = 20;
        }
        
        pdf.setFontSize(12);
        pdf.text('Performance Table:', 20, yPosition);
        yPosition += 10;
        
        pdf.setFontSize(10);
        
        // Table headers with background
        pdf.setFillColor(200, 200, 200);
        pdf.rect(20, yPosition - 2, 170, 8, 'F');
        pdf.setTextColor(0, 0, 0);
        
        pdf.text('Framework', 25, yPosition + 4);
        pdf.text('Algorithm', 70, yPosition + 4);
        pdf.text('Score', 140, yPosition + 4);
        yPosition += 10;
        
        // Table rows with alternating colors
        currentData.performance_table.forEach((row, index) => {
          if (yPosition > 270) {
            pdf.addPage();
            yPosition = 20;
          }
          
          // Alternating row colors
          if (index % 2 === 0) {
            pdf.setFillColor(245, 245, 245);
            pdf.rect(20, yPosition - 2, 170, 8, 'F');
          }
          
          pdf.text(row.Framework || '', 25, yPosition + 4);
          
          // Truncate long algorithm names
          const algorithm = row.Algorithm || '';
          const truncatedAlgorithm = algorithm.length > 20 ? algorithm.substring(0, 20) + '...' : algorithm;
          pdf.text(truncatedAlgorithm, 70, yPosition + 4);
          
          pdf.text(row.Score?.toString() || 'N/A', 140, yPosition + 4);
          yPosition += 8;
        });
        yPosition += 10;
      }

      // Add graph if exists
      if (currentData.graph_link?.graph_jpg) {
        console.log('Adding graph to PDF:', currentData.graph_link.graph_jpg);
        try {
          const API_BASE = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";
          
          if (yPosition + 80 > 280) {
            pdf.addPage();
            yPosition = 20;
          }

          pdf.setFontSize(12);
          pdf.text('Graph:', 20, yPosition);
          yPosition += 10;
          
          // Create a canvas to load and convert the image
          const canvas = document.createElement('canvas');
          const ctx = canvas.getContext('2d');
          const img = new Image();
          img.crossOrigin = 'anonymous';
          
          await new Promise((resolve, reject) => {
            img.onload = () => {
              try {
                canvas.width = img.width;
                canvas.height = img.height;
                ctx.drawImage(img, 0, 0);
                
                // Convert canvas to base64
                const imgData = canvas.toDataURL('image/jpeg', 0.8);
                
                // Calculate dimensions to fit in PDF
                const imgWidth = 170;
                const imgHeight = (img.height * imgWidth) / img.width;
                const finalHeight = Math.min(imgHeight, 150);
                
                // Add image to PDF
                pdf.addImage(imgData, 'JPEG', 20, yPosition, imgWidth, finalHeight);
                yPosition += finalHeight + 10;
                
                console.log('Graph successfully added to PDF');
                resolve();
              } catch (error) {
                console.error('Error processing image:', error);
                // Add text indicating graph was not loaded
                pdf.setFontSize(10);
                pdf.text('Graph could not be loaded', 20, yPosition);
                yPosition += 10;
                resolve();
              }
            };
            img.onerror = (error) => {
              console.error('Error loading image:', error);
              // Add text indicating graph was not loaded
              pdf.setFontSize(10);
              pdf.text('Graph could not be loaded', 20, yPosition);
              yPosition += 10;
              resolve();
            };
            img.src = `${API_BASE}${currentData.graph_link.graph_jpg}`;
          });

        } catch (error) {
          console.error('Error adding graph to PDF:', error);
          // Add text indicating graph was not loaded
          pdf.setFontSize(10);
          pdf.text('Graph could not be loaded', 20, yPosition);
          yPosition += 10;
        }
      }

      // Add data table info
      if (currentData.table && currentData.table.length > 0) {
        console.log('Adding data table to PDF:', currentData.table.length, 'rows');
        if (yPosition + 20 > 280) {
          pdf.addPage();
          yPosition = 20;
        }
        
        pdf.setFontSize(12);
        pdf.text('Data Table:', 20, yPosition);
        yPosition += 10;
        pdf.setFontSize(10);
        pdf.text(`Total Records: ${currentData.table.length}`, 20, yPosition);
        yPosition += 10;
        
        // Add first few rows as sample
        if (currentData.table.length > 0) {
          const headers = Object.keys(currentData.table[0]);
          const sampleRows = currentData.table.slice(0, 10);
          
          pdf.text('Sample Data (first 10 rows):', 20, yPosition);
          yPosition += 10;
          
          // Create table with proper spacing
          const columnWidth = 170 / headers.length;
          
          // Headers with background
          pdf.setFillColor(200, 200, 200);
          pdf.rect(20, yPosition - 2, 170, 8, 'F');
          pdf.setTextColor(0, 0, 0);
          
          let xPosition = 20;
          headers.forEach((header, index) => {
            const headerText = header.length > 12 ? header.substring(0, 12) + '...' : header;
            pdf.text(headerText, xPosition + 2, yPosition + 4);
            xPosition += columnWidth;
          });
          yPosition += 10;
          
          // Sample rows with alternating colors
          sampleRows.forEach((row, rowIndex) => {
            if (yPosition > 270) {
              pdf.addPage();
              yPosition = 20;
            }
            
            // Alternating row colors
            if (rowIndex % 2 === 0) {
              pdf.setFillColor(245, 245, 245);
              pdf.rect(20, yPosition - 2, 170, 8, 'F');
            }
            
            xPosition = 20;
            headers.forEach((header) => {
              const value = row[header]?.toString() || '';
              const cellText = value.length > 12 ? value.substring(0, 12) + '...' : value;
              pdf.text(cellText, xPosition + 2, yPosition + 4);
              xPosition += columnWidth;
            });
            yPosition += 8;
          });
          
          if (currentData.table.length > 10) {
            yPosition += 5;
            pdf.text(`... and ${currentData.table.length - 10} more rows`, 20, yPosition);
          }
        }
      }

      // Add spacing between sections
      if (i < dataKeys.length - 1) {
        yPosition += 15;
      }
    }

    // Save the PDF
    console.log('Saving PDF with filename:', fileName);
    pdf.save(fileName);
    console.log('PDF generation completed successfully');
  } catch (error) {
    console.error('Error generating PDF:', error);
  }
};
