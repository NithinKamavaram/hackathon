/**
 * Live agent activity visualization
 */

import React from 'react';
import { 
  Brain, 
  Code, 
  Search, 
  CheckCircle, 
  AlertTriangle 
} from 'lucide-react';

const AgentActivity = ({ agents }) => {
  const getAgentIcon = (agentName) => {
    const icons = {
      'RequirementsAgent': Brain,
      'ContextAgent': Search,
      'BuilderAgent': Code,
      'QualityAgent': CheckCircle,
      'EscalationAgent': AlertTriangle
    };
    return icons[agentName] || Brain;
  };

  const getStatusColor = (status) => {
    const colors = {
      'idle': 'gray',
      'working': 'blue',
      'completed': 'green',
      'failed': 'red'
    };
    return colors[status] || 'gray';
  };

  const getStatusSymbol = (status) => {
    const symbols = {
      'idle': '○',
      'working': '◐',
      'completed': '●',
      'failed': '✗'
    };
    return symbols[status] || '○';
  };

  return (
    <div className="agent-activity">
      <h2>Live Agent Activity</h2>
      <div className="agents-list">
        {agents.map((agent) => {
          const Icon = getAgentIcon(agent.name);
          const statusColor = getStatusColor(agent.status);
          
          return (
            <div
              key={agent.name}
              className={`agent-card agent-${statusColor}`}
            >
              <div className="agent-header">
                <Icon size={24} />
                <span className="agent-name">
                  {agent.name}
                </span>
                <span className="agent-status-symbol">
                  {getStatusSymbol(agent.status)}
                </span>
              </div>
              
              <div className="agent-activity-text">
                {agent.activity || 'Waiting...'}
              </div>

              {agent.progress > 0 && (
                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{ width: `${agent.progress}%` }}
                  />
                </div>
              )}

              {agent.payment && (
                <div className="agent-payment">
                  💰 ${agent.payment}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default AgentActivity;
