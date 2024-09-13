import React from 'react';
import { useParams, Link } from 'react-router-dom';
import blogData from './blogData.json'; // Adjust path if needed

interface Blog {
  id: number;
  title: string;
  summary: string;
  content: string;
}

const BlogDetail: React.FC = () => {
  const { blogId } = useParams<{ blogId: string }>();
  console.log('Blog ID from URL:', blogId); // Debugging line

  if (!blogId) {
    return <p>No blog ID provided</p>;
  }

  // Ensure blogId is a number and check for valid conversion
  const blogIdNumber = parseInt(blogId, 10);
  console.log('Parsed Blog ID Number:', blogIdNumber); // Debugging line

  if (isNaN(blogIdNumber)) {
    return <p>Invalid blog ID</p>;
  }

  const blog = blogData.find((b: Blog) => b.id === blogIdNumber);
  console.log('Blog Data:', blog); // Debugging line

  if (!blog) {
    return <p>Blog not found</p>;
  }

  return (
    <div className="bg-gray-100 flex min-h-screen">
      <div className="container mx-auto p-8">
        <div className="bg-white rounded-lg shadow-md p-8">
          <h1 className="text-3xl font-bold mb-4">{blog.title}</h1>
          <div className="text-lg mb-6">
            <p>{blog.content}</p>
          </div>
          <Link to="/blog" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Back to Blog List
          </Link>
        </div>
      </div>
    </div>
  );
};

export default BlogDetail;
