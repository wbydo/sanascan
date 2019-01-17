import { Dispatch } from "redux";

import { RootState } from "..";

export interface Store {
  getState: () => RootState;
  dispatch: Dispatch;
}
