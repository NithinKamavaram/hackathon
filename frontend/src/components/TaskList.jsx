/**
 * Task list with status
 */

import React from 'react';
import { 
  CheckCircle, 
  Clock, 
  AlertCircle, 
  XCircle,
  ExternalLink 
} from 'lucide-react';

const TaskList = ({ tasks, onTaskClick }) => {
  const getStatusIcon = (decision) => {
    const icons = {
      'COMPLETE': CheckCircle,
      'ESCALATE': AlertCircle,
      'processing': Clock,
      'failed': XCircle
    };
    return icons[decision] || Clock;
  };

  const getStatusColor = (decision) => {
    const colors = {
      'COMPLETE': 'green',
      'ESCALATE': 'yellow',
      'processing': 'blue',
      'failed': 'red'
    };
    return colors[decision] || 'gray';
  };

  const formatTimeAgo = (timestamp) => {
    if (!timestamp) return 'just now';
    const now = new Date();
    const then = new Date(timestamp);
    const seconds = Math.floor((now - then) / 1000);

    if (seconds < 60) return `${seconds}s ago`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    return `${Math.floor(seconds / 86400)}d ago`;
  };

  return (
    <div className="task-list">
      <h2>Recent Tasks</h2>
      <div className="tasks">
        {tasks.length === 0 ? (
          <div className="empty-state">
            <p>No tasks yet. Submit your first task above!</p>
          </div>
        ) : (
          tasks.slice().reverse().map((task, idx) => {
            const StatusIcon = getStatusIcon(task.final_decision || 'processing');
            const statusColor = getStatusColor(task.final_decision || 'processing');

            return (
              <div
                key={idx}
                className={`task-card task-${statusColor}`}
                onClick={() => onTaskClick && onTaskClick(task)}
              >
                <div className="task-header">
                  <StatusIcon size={20} />
                  <span className="task-status">
                    {task.final_decision || 'Processing'}
                  </span>
                  <span className="task-time">
                    {formatTimeAgo(task.timestamp)}
                  </span>
                </div>

                <div className="task-description">
                  {task.task_description?.slice(0, 100) || 'No description'}
                  {task.task_description?.length > 100 && '...'}
                </div>

                {task.final_decision && (
                  <div className="task-result">
                    {task.final_decision === 'COMPLETE' && (
                      <span className="result-success">
                        ✓ Completed by AI
                      </span>
                    )}
                    {task.final_decision === 'ESCALATE' && (
                      <span className="result-escalated">
                        ⚠ Escalated to human expert
                      </span>
                    )}
                    {task.error && (
                      <span className="result-failed">
                        ✗ Failed: {task.error}
                      </span>
                    )}
                  </div>
                )}

                <div className="task-footer">
                  <span className="task-id">
                    {task.execution_time_ms}ms • {task.tokens_used || 0} tokens
                  </span>
                  <button className="view-details">
                    Details <ExternalLink size={14} />
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default TaskList;
