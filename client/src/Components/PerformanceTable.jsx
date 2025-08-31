
import "ag-grid-community/styles/ag-grid.css"; 
import "ag-grid-community/styles/ag-theme-quartz.css"; 
import { AgGridReact } from "ag-grid-react"; 
import React, { useMemo, useRef } from "react";

function PerformanceTable({ rowData }) {
  const gridApi = useRef(null);
  const colDefs =
    rowData && rowData.length > 0
      ? Object.keys(rowData[0]).map((val) => ({ field: val }))
      : [];

  const defaultColDef = useMemo(
    () => ({
      filter: true, 
      resizable: true,
      minWidth: 150,
    }),
    []
  );

  const onGridReady = (params) => {
    gridApi.current = params.api;
  };
  return (
    <div className="ag-theme-quartz !w-full" style={{ height: 250, width: "100%" }}>
      <AgGridReact
        onGridReady={onGridReady}
        onFirstDataRendered={onGridReady}
        rowData={rowData}
        columnDefs={colDefs}
        defaultColDef={{
          ...defaultColDef,
        }}
        // pagination={true}
        // paginationPageSize={5}
        // paginationPageSize={3}
        // paginateChildRows={5}
        autoSizeStrategy={{ type: "fitGridWidth" }}
      />
    </div>
  );
}

export default PerformanceTable;
