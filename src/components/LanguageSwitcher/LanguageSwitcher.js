/* eslint-disable no-shadow */

import React, {PropTypes} from 'react';
import {connect} from 'react-redux';
import {setLocale} from '../../actions/intl';

function LanguageSwitcher({currentLocale, availableLocales, setLocale}) {
  const isSelected = (locale) => locale === currentLocale;
  const localeDict = {
    'da-DK': 'Dansk',
  };
  const localeName = (locale) => localeDict[locale] || locale;
  if (localeDict.length > 1) {
    return (
      <div>
        {availableLocales.map(locale => (
          <span key={locale}>
            {isSelected(locale) ? (
              <span>{localeName(locale)}</span>
            ) : (
              <a
                href={`?lang=${locale}`}
                onClick={(e) => {
                  setLocale({locale});
                  e.preventDefault();
                }}
              >{localeName(locale)}</a>
            )}
            {' '}
          </span>
        ))}
      </div>
    );
  } else {
    return <div/>;
  }
}

LanguageSwitcher.propTypes = {
  currentLocale: PropTypes.string.isRequired,
  availableLocales: PropTypes.arrayOf(PropTypes.string).isRequired,
  setLocale: PropTypes.func.isRequired,
};

const mapState = (state) => ({
  availableLocales: state.runtime.availableLocales,
  currentLocale: state.intl.locale,
});

const mapDispatch = {
  setLocale,
};

export default connect(mapState, mapDispatch)(LanguageSwitcher);
