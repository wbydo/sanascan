import * as types from "./types";

export const setActive = (isActive: boolean) => {
  return {
    error: false,
    payload: { isActive },
    type: types.SET_ACTIVE,
  };
};
