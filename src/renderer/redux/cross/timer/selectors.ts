import { RootState } from "../..";

export const selector = (state: RootState) => {
  return {
    scanSpeed: state.timer.scanSpeed,
  };
};
