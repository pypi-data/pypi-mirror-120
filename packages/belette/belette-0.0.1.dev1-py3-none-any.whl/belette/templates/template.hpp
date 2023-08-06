///
/// Contains licensing information for the project
///
/// {{ generated_file_warning | replace('\n', '\n/// ')}}
///

#pragma once

#include <map>
#include <string>
#include <vector>
#include <iostream>

struct open_source_package_t {
  std::string name;
  std::string version;
  std::string license_identifier; ///< SPDX license identifier
  std::string homepage;
};

inline bool operator==(const open_source_package_t& l, const open_source_package_t& r) {
  return (l.name == r.name)
    && (l.version == r.version)
    && (l.license_identifier == r.license_identifier)
    && (l.homepage == r.homepage);
}

inline bool operator!=(const open_source_package_t& l, const open_source_package_t& r) {
  return !(l == r);
}

std::ostream& operator<<(std::ostream& os, const open_source_package_t& p) {
  os << "{" << p.name << ", " << p.version << ", " << p.license_identifier
     << ", " << p.homepage << "}";
  return os;
}

/// Returns the full text of a license, given its SPDX identifier
inline std::string get_license_text(std::string license_identifier) {
  static std::map<std::string, std::string> license_texts = {
    {% for id in licenses %}
    { "{{ id }}", R"({{ licenses[id] }})" },
    {% endfor %}
  };

  return license_texts[license_identifier];
}

/// Returns a vector of all open-source dependencies of this application
inline std::vector<open_source_package_t> get_open_source_packages() {
  static std::vector<open_source_package_t> packages = {
    {% for package in packages %}
    {"{{ package.name }}", "{{ package.version }}",
     "{{ package.license }}", "{{ package.homepage }}"},
    {% endfor %}
  };

  return packages;
}
