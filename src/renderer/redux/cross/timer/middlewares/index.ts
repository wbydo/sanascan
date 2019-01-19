import { Dispatch } from "redux";

import * as types from "../types";
import * as actions from "../actions";
import { selector } from "../selectors";

import { Store } from "../../util";

import { Action as _Action } from "../../../util";
import { actions as cursolActions } from "../../../state/cursol";
import { actions as timerActions } from "../../../state/timer";

type Action = _Action<typeof actions>;

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
        store.dispatch(timerActions.setActive(true));
        break;

      case types.KILL:
        next(action);
        this.kill();
        store.dispatch(timerActions.setActive(false));
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
