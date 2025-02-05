package com.jav.server.service.base;

import com.jav.server.entity.base.Label;

public interface LabelService {
    void saveLabel(Label label);

    Label queryLabelById(Integer id);

    Label queryLabelByName(String name);
    
}
