import { RootState } from ".";

export const selectors = (state: RootState) => {
  return {
    activeColumn: state.cursol.activeColumn,
    activeRow: state.cursol.activeRow,
    configureWindowIsActive: state.configWindow.isActive,
    configureWindowScanSpeed: state.configWindow.scanSpeed,
    cursolDirection: state.cursol.direction,
    cursolMode: state.cursol.mode,
    developerMode: state.developerMode,
    result: state.estimator.result,
    timerScanSpeed: state.timer.scanSpeed,
  };
};
