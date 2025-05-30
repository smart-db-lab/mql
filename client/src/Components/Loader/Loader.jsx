import React from 'react'

export default function Loader() {
  return (
   <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/50 backdrop-blur-sm">
  <div className="flex flex-col items-center space-y-4">
    <div className="w-14 h-14 rounded-full border-4 border-t-blue-500 border-b-blue-500 border-l-transparent border-r-transparent animate-spin shadow-lg"></div>
    <p className="text-white text-lg font-medium animate-pulse">Loading...</p>
  </div>
</div>

  )
}
