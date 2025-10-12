/**
 * Status bar showing system health
 */

import React from 'react';
import { Activity, Zap, DollarSign } from 'lucide-react';

const StatusBar = ({ status }) => {
  return (
    <div className="status-bar">
      <div className="status-item">
        <Activity size={16} />
        <span>Status: {status?.status || 'loading'}</span>
      </div>

      <div className="status-item">
        <Zap size={16} />
        <span>
          {status?.agents_count || 5} agents ready
        </span>
      </div>

      <div className="status-item">
        <DollarSign size={16} />
        <span>
          Swarm: {status?.swarm_available ? 'Active' : 'Mock Mode'}
        </span>
      </div>

      <div className="status-version">
        v{status?.version || '1.0.0'}
      </div>
    </div>
  );
};

export default StatusBar;
