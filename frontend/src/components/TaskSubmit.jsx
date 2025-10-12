/**
 * Task submission form with GitHub URL support
 */

import React, { useState } from 'react';
import { Send, Github } from 'lucide-react';

const TaskSubmit = ({ onTaskSubmitted }) => {
  const [description, setDescription] = useState('');
  const [githubUrl, setGithubUrl] = useState('');
  const [requirements, setRequirements] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (description.length < 10) {
      setError('Description must be at least 10 characters');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await onTaskSubmitted(description, githubUrl, requirements);
      setDescription('');
      setGithubUrl('');
      setRequirements('');
    } catch (err) {
      setError(err.message || 'Failed to submit task');
    } finally {
      setLoading(false);
    }
  };

  // Example tasks
  const examples = [
    {
      task: "Create a function to calculate fibonacci numbers",
      github: "",
      requirements: ""
    },
    {
      task: "Add error handling to the login function",
      github: "https://github.com/your-org/your-repo",
      requirements: "Use try-catch blocks, log errors, return user-friendly messages"
    },
    {
      task: "Implement pagination for the user list",
      github: "",
      requirements: "Support page size configuration, add next/prev buttons"
    }
  ];

  const loadExample = (example) => {
    setDescription(example.task);
    setGithubUrl(example.github);
    setRequirements(example.requirements);
  };

  return (
    <div className="task-submit">
      <h2>🚀 Submit New Task</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="description">
            Task Description <span className="required">*</span>
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe the bug fix or feature you need in natural language..."
            rows={4}
            disabled={loading}
            className="form-control"
          />
          <small>{description.length}/5000 characters</small>
        </div>

        <div className="form-group">
          <label htmlFor="githubUrl">
            <Github size={16} style={{ verticalAlign: 'middle', marginRight: '5px' }} />
            GitHub Repository URL (Optional)
          </label>
          <input
            id="githubUrl"
            type="url"
            value={githubUrl}
            onChange={(e) => setGithubUrl(e.target.value)}
            placeholder="https://github.com/username/repository"
            disabled={loading}
            className="form-control"
          />
          <small>Provide a GitHub URL to analyze your codebase for context</small>
        </div>

        <div className="form-group">
          <label htmlFor="requirements">Additional Requirements (Optional)</label>
          <textarea
            id="requirements"
            value={requirements}
            onChange={(e) => setRequirements(e.target.value)}
            placeholder="Any specific requirements, constraints, or preferences..."
            rows={3}
            disabled={loading}
            className="form-control"
          />
        </div>

        {/* Example tasks */}
        <div className="example-tasks">
          <p><strong>📝 Example tasks:</strong></p>
          {examples.map((example, idx) => (
            <button
              key={idx}
              type="button"
              className="example-btn"
              onClick={() => loadExample(example)}
              disabled={loading}
            >
              {example.task}
              {example.github && <Github size={12} style={{ marginLeft: '5px' }} />}
            </button>
          ))}
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || description.length < 10}
          className="btn btn-primary"
        >
          <Send size={16} />
          {loading ? 'Processing...' : 'Process Task'}
        </button>
      </form>
    </div>
  );
};

export default TaskSubmit;
