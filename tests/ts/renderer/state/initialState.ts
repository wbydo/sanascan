import { reducer } from "sanascan/renderer/state";

export const initialState = reducer(undefined, { type: "@@INIT" });
