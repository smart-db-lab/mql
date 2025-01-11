import "ag-grid-community/styles/ag-grid.css"; 
import "ag-grid-community/styles/ag-theme-quartz.css"; 
import { AgGridReact } from "ag-grid-react"; 
import React, { useMemo, useRef } from "react";

function AgGridTable({ rowData }) {
  const gridApi = useRef(null);
  //correct but not working for ( . ) in column name
  // const colDefs =
  //   rowData && rowData.length > 0
  //     ? Object.keys(rowData[0]).map((val) => ({ field: val }))
  //     : [];
  const colDefs =
    rowData && rowData.length > 0
      ? Object.keys(rowData[0]).map((val) => ({
          headerName: val.replace(/\./g, "_"), 
          field: val.replace(/\./g, "_"), 
        }))
      : [];

  // Preprocess row data (replace dots with underscores in keys)
  const sanitizedRowData = rowData.map((row) =>
    Object.fromEntries(
      Object.entries(row).map(([key, value]) => [key.replace(/\./g, "_"), value])
    )
  );
  const defaultColDef = useMemo(
    () => ({
      filter: true, // Enable filtering on all columns
      resizable: true,
      minWidth: 150,
    }),
    []
  );

  const onGridReady = (params) => {
    gridApi.current = params.api;
  };
  return (
    <div className="ag-theme-quartz !w-full" style={{ height: 330, width: "100%" }}>
      {/* The AG Grid component */}
      <AgGridReact
        onGridReady={onGridReady}
        onFirstDataRendered={onGridReady}
        rowData={sanitizedRowData}
        columnDefs={colDefs}
        defaultColDef={{
          ...defaultColDef,
        }}
        pagination={true}
        paginationPageSize={5}
        // paginationPageSize={3}
        // paginateChildRows={5}
        autoSizeStrategy={{ type: "fitGridWidth" }}
      />
    </div>
  );
}

export default AgGridTable;
