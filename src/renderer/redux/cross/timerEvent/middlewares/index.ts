import { Dispatch } from "redux";

import * as types from "../types";
import * as actions from "../actions";
import { selector } from "../selectors";

import { actions as cursolActions } from "../../../state/cursol";

import { Action as _Action } from "../../../util";

import { RootState } from "../../..";

type Action = _Action<typeof actions>;

export interface Store {
  getState: () => RootState;
  dispatch: Dispatch;
}

class SanascanTimer {
  private timeout: ReturnType<typeof setInterval> | null = null;

  public middleware
      = (store: Store) => (next: Dispatch) => (action: Action) => {

    switch (action.type) {
      case types.START:
        next(action);
        store.dispatch(actions.kill());

        const { scanSpeed } = selector(store.getState());
        this.start(store.dispatch, scanSpeed);
        break;

      case types.KILL:
        next(action);
        this.kill();
        break;

      default:
        next(action);
    }
  }

  private kill = () => {
    clearInterval(this.timeout!);
    if (this.timeout !== null) {
      this.timeout = null;
    }
  }

  private start = (storeDispatch: Dispatch, scanSpeed: number) => {
    this.timeout = setInterval(
      () => storeDispatch(cursolActions.increment()),
      scanSpeed,
    );
  }

}

export const middlewares = [
  new SanascanTimer().middleware,
];
