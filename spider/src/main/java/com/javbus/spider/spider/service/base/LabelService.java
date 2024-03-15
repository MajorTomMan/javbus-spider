package com.javbus.spider.spider.service.base;

import com.javbus.spider.spider.entity.base.Label;

public interface LabelService {
    void saveLabel(Label label);

    Label queryLabelById(Integer id);

    Label queryLabelByName(String name);
    
}
