import { reducer } from "sanascan/renderer/redux";

export const initialState = reducer(undefined, { type: "@@INIT" });
