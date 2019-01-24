import {
  Component,
  OnInit,
  ChangeDetectionStrategy,
  ChangeDetectorRef
} from '@angular/core';
import { Store, select } from '@ngrx/store';
import { Observable } from 'rxjs';

import { ROUTE_ANIMATIONS_ELEMENTS, selectCurrentLocation } from '@app/core';

import {
  ActionSettingsChangeAnimationsElements,
  ActionSettingsChangeAnimationsPage,
  ActionSettingsChangeAutoNightMode,
  ActionSettingsChangeLanguage,
  ActionSettingsChangeTheme,
  ActionSettingsChangeStickyHeader,
  ActionSettingsRetrieve,
  ActionSettingsUpdate
} from '../settings.actions';
import { SettingsState, State } from '../settings.model';
import { selectSettings, selectLocationDetails } from '../settings.selectors';
import { Address } from '@app/shared/models/address';
import { LocationMetadata } from '@app/shared/models/location';

@Component({
  selector: 'lynx-settings',
  templateUrl: './settings-container.component.html',
  styleUrls: ['./settings-container.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class SettingsContainerComponent implements OnInit {
  routeAnimationsElements = ROUTE_ANIMATIONS_ELEMENTS;
  settings$: Observable<SettingsState>;
  currentLocID: number;

  //Begin New settings
  address: Address = new Address();
  locationMetadata: LocationMetadata = new LocationMetadata();

  // End new setting

  themes = [
    { value: 'DEFAULT-THEME', label: 'blue' },
    { value: 'LIGHT-THEME', label: 'light' },
    { value: 'NATURE-THEME', label: 'nature' },
    { value: 'BLACK-THEME', label: 'dark' }
  ];

  languages = [
    { value: 'en', label: 'en' },
    { value: 'de', label: 'de' },
    { value: 'sk', label: 'sk' },
    { value: 'fr', label: 'fr' },
    { value: 'es', label: 'es' },
    { value: 'pt-br', label: 'pt-br' }
  ];

  constructor(private store: Store<State>) { }

  ngOnInit() {
    // this.address.address1 ="3 woodward way";
    this.settings$ = this.store.pipe(select(selectSettings));
    this.store.pipe(select(selectCurrentLocation)).subscribe(loc => {

      // TODO: remove this
      if (loc != null)
        this.currentLocID = loc.locationid
      else
        this.currentLocID = 1

      this.store.dispatch(new ActionSettingsRetrieve({ locID: this.currentLocID }));
    })

    this.store.pipe(select(selectLocationDetails)).subscribe(settings => {
      this.address.fromSettings(settings);
      this.locationMetadata.fromSettings(settings);
    });
  }

  onLanguageSelect({ value: language }) {
    this.store.dispatch(new ActionSettingsChangeLanguage({ language }));
  }

  onThemeSelect({ value: theme }) {
    this.store.dispatch(new ActionSettingsChangeTheme({ theme }));
  }

  onAutoNightModeToggle({ checked: autoNightMode }) {
    this.store.dispatch(
      new ActionSettingsChangeAutoNightMode({ autoNightMode })
    );
  }

  onStickyHeaderToggle({ checked: stickyHeader }) {
    this.store.dispatch(new ActionSettingsChangeStickyHeader({ stickyHeader }));
  }

  onPageAnimationsToggle({ checked: pageAnimations }) {
    this.store.dispatch(
      new ActionSettingsChangeAnimationsPage({ pageAnimations })
    );
  }

  onElementsAnimationsToggle({ checked: elementsAnimations }) {
    this.store.dispatch(
      new ActionSettingsChangeAnimationsElements({ elementsAnimations })
    );
  }
  updateAddress() {
    console.log(this.address.toSettings());
    var addrJson = this.address.toSettings();
    console.log("Stage 2" + this.address.toSettings());
    this.store.dispatch(new ActionSettingsUpdate({ data: addrJson, locID: this.currentLocID }));

  }

  updateLocMeta() {
    var locMetaJson = this.locationMetadata.toSettings();
    this.store.dispatch(new ActionSettingsUpdate({ data: locMetaJson, locID: this.currentLocID }));

  }
}
