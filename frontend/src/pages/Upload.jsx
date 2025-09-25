import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { api } from '../lib/api';
import LoadingSpinner from '../components/LoadingSpinner';

const Upload = () => {
  const [files, setFiles] = useState({
    reviews: null,
    returns: null,
  });
  const [uploading, setUploading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (type, file) => {
    setFiles(prev => ({ ...prev, [type]: file }));
    setUploadSuccess(false);
  };

  const validateFile = (file, expectedColumns) => {
    return new Promise((resolve, reject) => {
      if (!file) {
        reject(new Error('File is required'));
        return;
      }

      if (!file.name.toLowerCase().endsWith('.csv')) {
        reject(new Error('File must be a CSV'));
        return;
      }

      // For now, just check file exists - server will validate columns
      resolve(true);
    });
  };

  const handleUpload = async () => {
    try {
      setUploading(true);

      // Validate files
      await validateFile(files.reviews, ['product_id', 'review_text', 'rating', 'date']);
      await validateFile(files.returns, ['product_id', 'return_reason_text', 'condition_flag', 'date']);

      // Create FormData
      const formData = new FormData();
      formData.append('reviews_csv', files.reviews);
      formData.append('returns_csv', files.returns);

      // Upload files
      const result = await api.post('/upload', formData);
      
      toast.success(`Successfully uploaded ${result.reviews_uploaded} reviews and ${result.returns_uploaded} returns!`);
      setUploadSuccess(true);
      
    } catch (error) {
      console.error('Upload failed:', error);
      toast.error(`Upload failed: ${error.message}`);
    } finally {
      setUploading(false);
    }
  };

  const handleProcess = async () => {
    try {
      setProcessing(true);
      
      const result = await api.post('/process', {});
      
      toast.success(`Processing complete! Analyzed ${result.products_processed} products.`);
      
      // Navigate to dashboard after successful processing
      setTimeout(() => {
        navigate('/dashboard');
      }, 1500);
      
    } catch (error) {
      console.error('Processing failed:', error);
      toast.error(`Processing failed: ${error.message}`);
    } finally {
      setProcessing(false);
    }
  };

  const canUpload = files.reviews && files.returns && !uploading;
  const canProcess = uploadSuccess && !processing;

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Upload Data Files</h1>
        <p className="text-gray-600 mb-8">
          Upload your CSV files containing product reviews and return reasons to get started.
        </p>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Reviews Upload */}
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Reviews CSV
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
                <input
                  type="file"
                  accept=".csv"
                  onChange={(e) => handleFileChange('reviews', e.target.files[0])}
                  className="hidden"
                  id="reviews-upload"
                />
                <label htmlFor="reviews-upload" className="cursor-pointer">
                  <div className="space-y-2">
                    <div className="text-gray-400">
                      <svg className="mx-auto h-12 w-12" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                    </div>
                    <div className="text-sm text-gray-600">
                      <span className="font-medium text-blue-600">Click to upload</span> or drag and drop
                    </div>
                    <div className="text-xs text-gray-500">
                      CSV files only
                    </div>
                  </div>
                </label>
              </div>
              {files.reviews && (
                <p className="mt-2 text-sm text-green-600">
                  ✓ {files.reviews.name}
                </p>
              )}
              <div className="mt-3 text-xs text-gray-500">
                <p className="font-medium">Required columns:</p>
                <ul className="list-disc list-inside mt-1 space-y-0.5">
                  <li>product_id</li>
                  <li>review_text</li>
                  <li>rating</li>
                  <li>date</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Returns Upload */}
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Returns CSV
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
                <input
                  type="file"
                  accept=".csv"
                  onChange={(e) => handleFileChange('returns', e.target.files[0])}
                  className="hidden"
                  id="returns-upload"
                />
                <label htmlFor="returns-upload" className="cursor-pointer">
                  <div className="space-y-2">
                    <div className="text-gray-400">
                      <svg className="mx-auto h-12 w-12" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                    </div>
                    <div className="text-sm text-gray-600">
                      <span className="font-medium text-blue-600">Click to upload</span> or drag and drop
                    </div>
                    <div className="text-xs text-gray-500">
                      CSV files only
                    </div>
                  </div>
                </label>
              </div>
              {files.returns && (
                <p className="mt-2 text-sm text-green-600">
                  ✓ {files.returns.name}
                </p>
              )}
              <div className="mt-3 text-xs text-gray-500">
                <p className="font-medium">Required columns:</p>
                <ul className="list-disc list-inside mt-1 space-y-0.5">
                  <li>product_id</li>
                  <li>return_reason_text</li>
                  <li>condition_flag</li>
                  <li>date</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-8 flex flex-col sm:flex-row gap-4">
          <button
            onClick={handleUpload}
            disabled={!canUpload}
            className={`flex-1 px-6 py-3 rounded-md font-medium transition-colors ${
              canUpload
                ? 'bg-blue-600 text-white hover:bg-blue-700'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            {uploading ? (
              <div className="flex items-center justify-center space-x-2">
                <LoadingSpinner size="small" text="" />
                <span>Uploading...</span>
              </div>
            ) : (
              'Upload Files'
            )}
          </button>

          <button
            onClick={handleProcess}
            disabled={!canProcess}
            className={`flex-1 px-6 py-3 rounded-md font-medium transition-colors ${
              canProcess
                ? 'bg-green-600 text-white hover:bg-green-700'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            {processing ? (
              <div className="flex items-center justify-center space-x-2">
                <LoadingSpinner size="small" text="" />
                <span>Processing...</span>
              </div>
            ) : (
              'Process Data'
            )}
          </button>
        </div>

        {/* Status Messages */}
        {uploadSuccess && (
          <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-md">
            <p className="text-green-800 text-sm">
              ✓ Files uploaded successfully! Click "Process Data" to analyze the feedback.
            </p>
          </div>
        )}

        {/* Instructions */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-md p-4">
          <h3 className="text-sm font-medium text-blue-800 mb-2">How it works:</h3>
          <ol className="list-decimal list-inside text-sm text-blue-700 space-y-1">
            <li>Upload your reviews and returns CSV files</li>
            <li>Click "Process Data" to analyze the feedback</li>
            <li>View results in the Dashboard</li>
            <li>Export detailed reports for specific products</li>
          </ol>
        </div>
      </div>
    </div>
  );
};

export default Upload;