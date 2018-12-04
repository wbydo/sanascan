import * as types from "./types";

export interface Action {
  error: boolean;
  type: string;
  payload: {
    status?: "start" | "done" | "error";
    id?: number;
  };
}

export const fetchId = (status: "start" | "done" | "error"): Action => {
  return {
    error: status === "error",
    payload: {
      status,
    },
    type: types.FETCH_ID,
  };
};

export const setId = (id: number): Action => {
  return {
    error: false,
    payload: {
      id,
    },
    type: types.SET_ID,
  };
};
