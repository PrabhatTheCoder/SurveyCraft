import React from 'react';
import { Link } from 'react-router-dom';
import blogData from './blogData.json'; // Assume this file contains your blog data

const BlogList = () => {
  return (
    <div className="bg-gray-100 blog flex min-h-screen">
      <div className="container mx-auto p-8">
        <div className="bg-white rounded-lg shadow-md p-8">
          <h1 className="text-3xl font-bold mb-8">Blog List</h1>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {blogData.map((blog) => (
              <Link to={`/blog/${blog.id}`} key={blog.id} className="bg-gray-200 rounded-lg p-6 shadow-md hover:bg-gray-300 transition duration-200">
                <h2 className="text-xl font-semibold">{blog.title}</h2>
                <p className="mt-4">{blog.summary}</p>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BlogList;
