/**
 * Result display component showing generated code and outputs
 */

import React, { useState } from 'react';
import { Copy, Check } from 'lucide-react';

const ResultDisplay = ({ result }) => {
  const [copied, setCopied] = useState(false);

  if (!result) return null;

  const handleCopy = () => {
    if (result.code) {
      navigator.clipboard.writeText(result.code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // Format final result - show complete output, only remove duplicate code blocks
  const formatFinalMessage = (text) => {
    if (!text || typeof text !== 'string') return '';

    // Remove markdown code blocks since they're shown separately above
    let formatted = text.replace(/```[\s\S]*?```/g, '[Code shown above]');

    // Return full text without truncation
    return formatted;
  };

  return (
    <div className="result-display">
      <h2>Task Results</h2>
      
      {/* Final Decision Banner */}
      <div className={`decision-banner decision-${result.final_decision?.toLowerCase()}`}>
        {result.final_decision === 'COMPLETE' ? (
          <>
            <span className="decision-icon">✓</span>
            <span className="decision-text">Task Completed by AI</span>
          </>
        ) : result.final_decision === 'ESCALATE' ? (
          <>
            <span className="decision-icon">⚠</span>
            <span className="decision-text">Task Escalated to Human Expert</span>
          </>
        ) : (
          <>
            <span className="decision-icon">◐</span>
            <span className="decision-text">Processing...</span>
          </>
        )}
      </div>

      {/* Task Description */}
      <div className="result-section">
        <h3>Task Description</h3>
        <p className="task-description-text">{result.task_description}</p>
      </div>

      {/* Agent Sequence */}
      {result.agent_sequence && result.agent_sequence.length > 0 && (
        <div className="result-section">
          <h3>Agent Pipeline</h3>
          <div className="agent-pipeline">
            {result.agent_sequence.map((agent, idx) => (
              <React.Fragment key={idx}>
                <span className="pipeline-agent">{agent}</span>
                {idx < result.agent_sequence.length - 1 && (
                  <span className="pipeline-arrow">→</span>
                )}
              </React.Fragment>
            ))}
          </div>
        </div>
      )}

      {/* Generated Code */}
      {result.code && (
        <div className="result-section">
          <div className="code-header">
            <h3>Generated Code</h3>
            <button onClick={handleCopy} className="copy-button">
              {copied ? <Check size={16} /> : <Copy size={16} />}
              {copied ? 'Copied!' : 'Copy'}
            </button>
          </div>
          <pre className="code-block">
            <code>{result.code}</code>
          </pre>
        </div>
      )}

      {/* Agent Outputs */}
      {result.agent_outputs && Object.keys(result.agent_outputs).length > 0 && (
        <div className="result-section">
          <h3>Agent Contributions</h3>
          <div className="agent-outputs">
            {Object.entries(result.agent_outputs).map(([agentName, output]) => (
              <div key={agentName} className="agent-output-card">
                <div className="agent-output-header">
                  <strong>{agentName}</strong>
                </div>
                <div className="agent-output-content">
                  {output.response && (
                    <p className="output-response">{output.response}</p>
                  )}
                  {output.handoff_message && (
                    <p className="output-handoff">
                      <em>Handoff: {output.handoff_message}</em>
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Execution Metrics */}
      <div className="result-section">
        <h3>Execution Metrics</h3>
        <div className="metrics-grid">
          <div className="metric-item">
            <span className="metric-label">Execution Time</span>
            <span className="metric-value">{result.execution_time_ms || 0}ms</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">Tokens Used</span>
            <span className="metric-value">{result.tokens_used || 0}</span>
          </div>
          {result.agent_sequence && (
            <div className="metric-item">
              <span className="metric-label">Agents Involved</span>
              <span className="metric-value">{result.agent_sequence.length}</span>
            </div>
          )}
        </div>
      </div>

      {/* Final Result/Message */}
      {result.final_result && (
        <div className="result-section">
          <h3>Final Output</h3>
          <div className="final-message">
            <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
              {formatFinalMessage(result.final_result)}
            </pre>
          </div>
        </div>
      )}

      {/* Error Display */}
      {result.error && (
        <div className="result-section error-section">
          <h3>Error</h3>
          <div className="error-content">
            {result.error}
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultDisplay;
