import React from "react";
import "./ProgressTracker.css";

/**
 * Step data structure
 * @property {number} id - Step identifier (1-based index)
 * @property {string} label - Text description of the step
 * @property {string} status - Current step status: "pending", "active", or "completed"
 */
type Step = {
  id: number;
  label: string;
  status: "pending" | "active" | "completed";
};

/**
 * ProgressTracker Component Props
 * @property {Step[]} steps - Array of steps with their status information
 * @property {number} currentStep - Current active step index (0-based)
 */
interface ProgressTrackerProps {
  steps: Step[];
  currentStep: number;
}

/**
 * ProgressTracker Component
 *
 * Displays a visual progress tracker with numbered steps and a progress bar.
 * Each step can be in pending, active, or completed state with appropriate styling.
 * The progress bar shows relative completion of the overall workflow.
 */
export const ProgressTracker: React.FC<ProgressTrackerProps> = ({
  steps,
  currentStep,
}) => {
  return (
    <div className="progress-tracker">
      {/* Horizontal progress bar with dynamic width based on current step */}
      <div className="progress-bar">
        <div
          className="progress-indicator"
          style={{
            width: `${(currentStep / (steps.length - 1)) * 100}%`,
          }}
        ></div>
      </div>

      {/* Step circles with numbers and labels */}
      <div className="steps-container">
        {steps.map((step) => (
          <div key={step.id} className={`step-item ${step.status}`}>
            <div className="step-number">{step.id}</div>
            <div className="step-label">{step.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
};
